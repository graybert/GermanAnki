const state = { cards: [], index: 0, answer: false };
const stage = document.querySelector('#card-stage');
const picker = document.querySelector('#card-picker');
const flip = document.querySelector('#flip');
let activeAudio = null;

const audioFiles = {
  1: ['ga_word_der_e415f41056.mp3', 'ga_f0001_der_e415f41056.mp3'],
  2: ['ga_word_und_2348896332.mp3', 'ga_f0002_und_2348896332.mp3'],
  3: ['ga_word_in_23fd2ce263.mp3', 'ga_f0003_in_23fd2ce263.mp3'],
  4: ['ga_word_sein_61000ca421.mp3', 'ga_f0004_sein_61000ca421.mp3'],
  5: ['ga_word_ein_affbd2f8e3.mp3', 'ga_f0005_ein_affbd2f8e3.mp3'],
  6: ['ga_word_haben_823cdecde0.mp3', 'ga_f0006_haben_823cdecde0.mp3'],
  7: ['ga_word_sie_a5100c5842.mp3', 'ga_f0007_sie_a5100c5842.mp3'],
  8: ['ga_word_werden_7a556b200f.mp3', 'ga_f0008_werden_7a556b200f.mp3'],
  9: ['ga_word_von_1838a59c44.mp3', 'ga_f0009_von_1838a59c44.mp3'],
  10: ['ga_word_ich_081fa3de4a.mp3', 'ga_f0010_ich_081fa3de4a.mp3'],
};

function playAudio(filename, speed = 1) {
  if (activeAudio) {
    activeAudio.pause();
    activeAudio.currentTime = 0;
  }
  activeAudio = new Audio(`../data/audio/test-v7-first-10/${filename}`);
  activeAudio.playbackRate = speed;
  activeAudio.play();
}

function configureAudio(card) {
  const files = audioFiles[card.frequency_rank];
  const unavailable = stage.querySelector('.audio-unavailable');
  if (!files) return;
  unavailable.hidden = true;
  const [wordFile, sentenceFile] = files;
  const wordButton = stage.querySelector('.word-audio');
  const sentenceButton = stage.querySelector('.sentence-audio');
  const speedControls = stage.querySelector('.web-speed-controls');
  wordButton.hidden = false;
  sentenceButton.hidden = false;
  speedControls.hidden = false;
  wordButton.addEventListener('click', () => playAudio(wordFile));
  sentenceButton.addEventListener('click', () => playAudio(sentenceFile));
  speedControls.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => playAudio(sentenceFile, Number(button.dataset.speed)));
  });
}

function valueText(value) {
  if (typeof value === 'string') return value;
  return Object.entries(value).map(([key, val]) => `${key.replaceAll('_', ' ')}: ${val}`).join(' · ');
}

function renderForms(forms) {
  if (!forms.length) return '';
  return `<table class="forms-table"><tbody>${forms.map((row, i) =>
    `<tr><th>Pattern ${i + 1}</th><td>${valueText(row)}</td></tr>`).join('')}</tbody></table>`;
}

function render() {
  const card = state.cards[state.index];
  const template = document.querySelector(state.answer ? '#back-template' : '#front-template');
  stage.replaceChildren(template.content.cloneNode(true));
  stage.querySelector('.target').textContent = card.target;
  configureAudio(card);
  if (state.answer) {
    stage.querySelector('.part-of-speech').textContent = card.part_of_speech;
    stage.querySelector('.meaning').textContent = card.meaning;
    stage.querySelector('.german-sentence').textContent = card.german_sentence;
    stage.querySelector('.english-sentence').textContent = card.english_sentence;
    stage.querySelector('.usage').textContent = card.usage_note;
    const examples = stage.querySelector('.examples-list');
    card.extra_examples.forEach((example) => {
      const item = document.createElement('details');
      item.className = 'example-item';
      const summary = document.createElement('summary');
      summary.textContent = example.german;
      const translation = document.createElement('div');
      translation.className = 'example-translation';
      translation.lang = 'en';
      translation.textContent = example.english;
      item.append(summary, translation);
      examples.append(item);
    });
    const forms = stage.querySelector('.forms');
    forms.innerHTML = renderForms(card.forms);
    if (!card.forms.length) stage.querySelector('.forms-section').hidden = true;
  }
  picker.value = String(state.index);
  document.querySelector('#counter').textContent = `${state.index + 1} of ${state.cards.length}`;
  document.querySelector('#status').textContent = state.answer ? 'Back' : 'Front';
  flip.textContent = state.answer ? 'Show front' : 'Show answer';
  history.replaceState(null, '', `#${card.frequency_rank}`);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function move(amount) {
  state.index = (state.index + amount + state.cards.length) % state.cards.length;
  state.answer = false;
  render();
}

async function start() {
  const batchPaths = [
    '../data/canonical/frequency-0001-0010.jsonl',
    '../data/canonical/frequency-0011-0050.jsonl',
    '../data/canonical/frequency-0051-0200.jsonl',
    '../data/canonical/frequency-0201-0500.jsonl',
    '../data/canonical/frequency-0501-1000.jsonl',
    '../data/canonical/frequency-1001-1500.jsonl',
  ];
  const orderPath = '../data/curriculum/current-order.json';
  const [responses, orderResponse] = await Promise.all([
    Promise.all(batchPaths.map((path) => fetch(path))),
    fetch(orderPath),
  ]);
  const failed = responses.find((response) => !response.ok);
  if (failed) throw new Error(`Could not load cards (${failed.status})`);
  if (!orderResponse.ok) {
    throw new Error(`Could not load curriculum order (${orderResponse.status})`);
  }
  const texts = await Promise.all(responses.map((response) => response.text()));
  state.cards = texts.flatMap((body) => body.trim().split(/\r?\n/).map(JSON.parse));
  const curriculum = await orderResponse.json();
  const orderById = new Map(
    curriculum.cards.map((entry) => [entry.semantic_id, entry.curriculum_order])
  );
  state.cards.sort((left, right) =>
    orderById.get(left.semantic_id) - orderById.get(right.semantic_id)
  );
  state.cards.forEach((card, index) => {
    const option = document.createElement('option');
    option.value = String(index);
    option.textContent = `${card.frequency_rank}. ${card.target}`;
    picker.append(option);
  });
  const requested = Number(location.hash.slice(1));
  const requestedIndex = state.cards.findIndex(card => card.frequency_rank === requested);
  if (requestedIndex >= 0) state.index = requestedIndex;
  render();
}

document.querySelector('#previous').addEventListener('click', () => move(-1));
document.querySelector('#next').addEventListener('click', () => move(1));
flip.addEventListener('click', () => { state.answer = !state.answer; render(); });
picker.addEventListener('change', () => { state.index = Number(picker.value); state.answer = false; render(); });
document.querySelector('#theme').addEventListener('click', () => document.body.classList.toggle('dark'));
document.addEventListener('keydown', (event) => {
  if (event.target.matches('select, button')) return;
  if (event.key === 'ArrowLeft') move(-1);
  if (event.key === 'ArrowRight') move(1);
  if (event.key === ' ') { event.preventDefault(); state.answer = !state.answer; render(); }
  if (event.key.toLowerCase() === 'd') document.body.classList.toggle('dark');
});

start().catch((error) => { stage.innerHTML = `<p class="load-error">${error.message}</p>`; });
