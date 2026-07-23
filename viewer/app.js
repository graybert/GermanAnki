const state = { cards: [], index: 0, answer: false };
const stage = document.querySelector('#card-stage');
const picker = document.querySelector('#card-picker');
const flip = document.querySelector('#flip');

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
