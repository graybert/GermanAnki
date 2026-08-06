# Detailed source catalog

58 sources, verified 2026-08-05. The CSV/JSON manifests are canonical; this file is the readable rendering.

## lcc_news_de_1m — Leipzig Corpora Collection – German News

- **Priority:** Tier 1
- **Direct link:** https://wortschatz.uni-leipzig.de/en/download/German
- **Organization/author:** Leipzig University, Wortschatz
- **Category / genre:** general corpus / news corpus
- **Major topics:** politics; business; local and international news; sports; culture
- **Register / CEFR:** edited neutral journalistic / B1–C1
- **German variety / modality:** DE-dominant Standard German / written
- **Format:** sentence text + token/frequency files in compressed archives
- **Approximate usable material:** Selectable 10K–1M sentence packages per release
- **Access / availability:** bulk_open — Direct archive links from the German download page
- **Rights/access notes:** Research corpus; retain source metadata and review the licence/readme bundled with each archive
- **Specific linguistic coverage:** Dense contemporary syntax, named entities, reporting verbs, temporal framing, indirect attribution
- **Main limitation:** Automatically collected; duplicates, boilerplate and occasional bad segmentation
- **Recommended scope:** Download one recent 1M News package; cap older releases at 250K each
- **Command/download hint:** `python tools/acquire.py fetch lcc_news_de_1m`

## lcc_web_de_1m — Leipzig Corpora Collection – German Web

- **Priority:** Tier 1
- **Direct link:** https://wortschatz.uni-leipzig.de/en/download/German
- **Organization/author:** Leipzig University, Wortschatz
- **Category / genre:** general corpus / mixed web prose
- **Major topics:** consumer information; organizations; hobbies; services; technology; practical prose
- **Register / CEFR:** mixed neutral/informal/formal / A2–C1
- **German variety / modality:** DE-dominant Standard German / written
- **Format:** sentence text + metadata/frequency files
- **Approximate usable material:** Selectable up to 1M sentences per package
- **Access / availability:** bulk_open — Direct archive links from the German download page
- **Rights/access notes:** Review archive licence/readme; use internally as reference corpus
- **Specific linguistic coverage:** Broad lexical and constructional variety beyond news
- **Main limitation:** Web noise, SEO, fragments, duplicated templates
- **Recommended scope:** Download one recent 1M Web package; aggressively filter boilerplate and low-quality domains
- **Command/download hint:** `python tools/acquire.py fetch lcc_web_de_1m`

## lcc_wikipedia_de_1m — Leipzig Corpora Collection – German Wikipedia

- **Priority:** Tier 1
- **Direct link:** https://wortschatz.uni-leipzig.de/en/download/German
- **Organization/author:** Leipzig University, Wortschatz
- **Category / genre:** general corpus / encyclopedic prose
- **Major topics:** science; history; geography; culture; people; institutions
- **Register / CEFR:** neutral expository / B1–C1
- **German variety / modality:** Standard German / written
- **Format:** sentence text + metadata/frequency files
- **Approximate usable material:** Selectable up to 1M sentences
- **Access / availability:** bulk_open — Direct archive links from the German download page
- **Rights/access notes:** Derived from Wikimedia; preserve attribution/licence metadata
- **Specific linguistic coverage:** Definitions, apposition, taxonomic language, cause/effect, descriptions
- **Main limitation:** Topic skew and encyclopedic style; fewer interactions
- **Recommended scope:** Download 1M package for easy processing even if full dewiki is also acquired
- **Command/download hint:** `python tools/acquire.py fetch lcc_wikipedia_de_1m`

## dewiki_dump — German Wikipedia full dump

- **Priority:** Tier 1
- **Direct link:** https://dumps.wikimedia.org/dewiki/latest/
- **Organization/author:** Wikimedia Foundation / German Wikipedia contributors
- **Category / genre:** encyclopedic corpus / encyclopedia articles
- **Major topics:** science; society; culture; geography; biographies; technical topics
- **Register / CEFR:** neutral formal expository / B1–C1
- **German variety / modality:** Standard German with some DACH coverage / written
- **Format:** MediaWiki XML bz2; optional multistream index
- **Approximate usable material:** Multi-million-sentence corpus; exact count depends on current dump and extraction
- **Access / availability:** bulk_open — Direct current dump files
- **Rights/access notes:** CC BY-SA/GFDL; preserve attribution and dump metadata
- **Specific linguistic coverage:** Long-form context, terminology, definitions, relative clauses, nominal style
- **Main limitation:** Markup, lists, citations, formulae, uneven article quality
- **Recommended scope:** Acquire pages-articles multistream dump; sample by topic and article quality rather than ingesting all sentences equally
- **Command/download hint:** `python tools/acquire.py fetch dewiki_dump`

## dewikivoyage_dump — German Wikivoyage dump

- **Priority:** Tier 1
- **Direct link:** https://dumps.wikimedia.org/dewikivoyage/latest/
- **Organization/author:** Wikimedia Foundation / Wikivoyage contributors
- **Category / genre:** practical travel corpus / travel guide
- **Major topics:** transport; accommodation; restaurants; directions; tourism; safety; local customs
- **Register / CEFR:** neutral practical, occasional informal advice / A2–B2
- **German variety / modality:** Standard German; DACH and worldwide destinations / written
- **Format:** MediaWiki XML bz2
- **Approximate usable material:** Tens of thousands of destination/guide sections
- **Access / availability:** bulk_open — Direct current dump files
- **Rights/access notes:** CC BY-SA; preserve attribution
- **Specific linguistic coverage:** Imperatives, recommendations, directional language, prices, opening hours, travel problems
- **Main limitation:** Template/list-heavy; stale details; proper-name density
- **Recommended scope:** Acquire full pages-articles dump, then retain prose paragraphs and practical notices
- **Command/download hint:** `python tools/acquire.py fetch dewikivoyage_dump`

## dewikibooks_dump — German Wikibooks dump

- **Priority:** Tier 2
- **Direct link:** https://dumps.wikimedia.org/dewikibooks/latest/
- **Organization/author:** Wikimedia Foundation / Wikibooks contributors
- **Category / genre:** educational corpus / open textbooks and manuals
- **Major topics:** languages; computing; science; crafts; study skills
- **Register / CEFR:** instructional to academic / A2–C1
- **German variety / modality:** Standard German / written
- **Format:** MediaWiki XML bz2
- **Approximate usable material:** Large collection of book chapters; post-filter size varies
- **Access / availability:** bulk_open — Direct current dump files
- **Rights/access notes:** CC BY-SA/GFDL; preserve attribution
- **Specific linguistic coverage:** Explanations, procedures, examples, definitions, didactic sequencing
- **Main limitation:** Quality and completion vary; markup and exercises
- **Recommended scope:** Acquire full dump; select mature books and prose-rich chapters
- **Command/download hint:** `python tools/acquire.py fetch dewikibooks_dump`

## dewikinews_dump — German Wikinews dump

- **Priority:** Tier 3
- **Direct link:** https://dumps.wikimedia.org/dewikinews/latest/
- **Organization/author:** Wikimedia Foundation / German Wikinews contributors
- **Category / genre:** news archive / citizen-edited news
- **Major topics:** politics; local affairs; international events; culture; sports
- **Register / CEFR:** neutral journalistic / B1–C1
- **German variety / modality:** Standard German / written
- **Format:** MediaWiki XML bz2
- **Approximate usable material:** About fourteen thousand articles in the project archive
- **Access / availability:** bulk_open — Direct dump files
- **Rights/access notes:** CC BY; preserve attribution
- **Specific linguistic coverage:** Short news reports, chronology and event narration
- **Main limitation:** Small and less current than major news corpora; variable editing
- **Recommended scope:** Acquire once as a bounded historical supplement, not a primary current-news source
- **Command/download hint:** `python tools/acquire.py fetch dewikinews_dump`

## bundestag_open_data — German Bundestag Open Data – plenary protocols

- **Priority:** Tier 1
- **Direct link:** https://www.bundestag.de/services/opendata
- **Organization/author:** German Bundestag
- **Category / genre:** official/political corpus / parliamentary debate and documents
- **Major topics:** laws; budgets; policy; government; society; foreign affairs
- **Register / CEFR:** formal spoken-to-written, argumentative / B2–C1
- **German variety / modality:** Germany Standard German / spoken transcript + written documents
- **Format:** XML and JSON; term-organized downloads
- **Approximate usable material:** All plenary protocols and printed papers from the first legislative term onward
- **Access / availability:** bulk_open — Official machine-readable downloads
- **Rights/access notes:** Official open-data terms; retain document IDs, date, speaker and term
- **Specific linguistic coverage:** Argumentation, rebuttal, reported positions, Konjunktiv, formal address, interjections, long syntax
- **Main limitation:** Political/topic skew; formulaic procedure; historical language in older terms
- **Recommended scope:** Download 19th–21st terms first; preserve speaker turns and stage directions
- **Command/download hint:** `python tools/acquire.py fetch bundestag_open_data`

## germaparl — GermaParl v2.3

- **Priority:** Tier 3
- **Direct link:** https://zenodo.org/records/15495748
- **Organization/author:** Political Data Science / corpus maintainers
- **Category / genre:** annotated political corpus / Bundestag plenary protocols
- **Major topics:** policy; legislation; parliamentary discourse
- **Register / CEFR:** formal spoken-to-written / B2–C1
- **German variety / modality:** Germany Standard German / annotated transcript
- **Format:** XML and CWB archives
- **Approximate usable material:** About 2.6 GB for the CWB archive in the current release
- **Access / availability:** restricted_request — Zenodo access request; downloadable after approval
- **Rights/access notes:** Access-controlled; follow record conditions and do not redistribute if prohibited
- **Specific linguistic coverage:** Linguistic annotation, speaker metadata, parliamentary discourse analysis
- **Main limitation:** Approval friction; overlaps raw Bundestag data
- **Recommended scope:** Request after raw Bundestag acquisition if annotations will materially improve retrieval
- **Command/download hint:** `manual: request access on Zenodo`

## gesetze_im_internet — Gesetze im Internet

- **Priority:** Tier 1
- **Direct link:** https://www.gesetze-im-internet.de/
- **Organization/author:** Federal Ministry of Justice / Federal Office of Justice
- **Category / genre:** legal/official corpus / federal statutes and regulations
- **Major topics:** civil; criminal; employment; tax; administration; transport; health
- **Register / CEFR:** highly formal legal / C1
- **German variety / modality:** Germany legal Standard German / written
- **Format:** HTML, PDF, EPUB and XML; complete-law ZIPs
- **Approximate usable material:** Hundreds of current federal laws and regulations
- **Access / availability:** bulk_open — Per-law downloads and XML ZIP files
- **Rights/access notes:** Official legal texts; preserve version/date; public availability does not automatically settle every downstream reuse question
- **Specific linguistic coverage:** Case government, legal modality, definitions, conditions, exceptions, nominalizations
- **Main limitation:** Very specialized and syntactically dense; not representative everyday prose
- **Recommended scope:** Acquire a balanced set of 50–100 high-impact laws plus XML metadata, not the entire legal universe initially
- **Command/download hint:** `python tools/acquire.py fetch gesetze_im_internet`

## austria_parliament — Austrian Parliament Open Data and stenographic protocols

- **Priority:** Tier 2
- **Direct link:** https://www.parlament.gv.at/services/opendata/
- **Organization/author:** Austrian Parliament
- **Category / genre:** regional official/political corpus / parliamentary debate
- **Major topics:** Austrian policy; administration; economy; society
- **Register / CEFR:** formal spoken-to-written / B2–C1
- **German variety / modality:** AT Standard German / spoken transcript + official written
- **Format:** open-data feeds/pages; stenographic full text
- **Approximate usable material:** Full text available for many legislative periods; large archive
- **Access / availability:** downloadable_manual — Official open-data and protocol pages
- **Rights/access notes:** Use official terms; label AT and preserve date/speaker
- **Specific linguistic coverage:** Austrian administrative vocabulary, discourse markers and regional standard usage
- **Main limitation:** Political skew; some access endpoints require custom harvesting
- **Recommended scope:** Sample recent Nationalrat debates to reach 3–4% of total corpus
- **Command/download hint:** `manual/API: inspect official open-data endpoints`

## swiss_official_bulletin — Swiss Parliament Official Bulletin

- **Priority:** Tier 2
- **Direct link:** https://www.parlament.ch/en/ratsbetrieb/official-bulletin
- **Organization/author:** Swiss Federal Assembly
- **Category / genre:** regional official/political corpus / verbatim parliamentary debate
- **Major topics:** Swiss policy; federalism; multilingual governance; law
- **Register / CEFR:** formal spoken-to-written / B2–C1
- **German variety / modality:** CH Standard German; some Swiss-specific vocabulary / spoken transcript + video
- **Format:** web transcripts and video
- **Approximate usable material:** Large multi-year archive
- **Access / availability:** downloadable_manual — Official searchable transcripts; downloads vary by interface
- **Rights/access notes:** Use official terms; label CH and preserve chamber/language/date
- **Specific linguistic coverage:** Swiss Standard German vocabulary, formal debate, interruptions and spoken syntax
- **Main limitation:** Multilingual proceedings; extraction needs language filtering
- **Recommended scope:** Sample recent German-language debates to 2–3% of corpus
- **Command/download hint:** `manual: export/search official bulletin`

## swiss_parliaments_corpus — Swiss Parliaments Corpus

- **Priority:** Tier 3
- **Direct link:** https://www.swisstext.org/swiss-parliaments-corpus/
- **Organization/author:** SwissText / research consortium
- **Category / genre:** regional speech corpus / parliamentary speech
- **Major topics:** cantonal and national politics
- **Register / CEFR:** formal and semi-formal spoken / B2–C1
- **German variety / modality:** Swiss German speech aligned with Standard German text / audio-aligned transcript
- **Format:** research dataset
- **Approximate usable material:** About 293 hours of speech in the published corpus
- **Access / availability:** bulk_or_request — Freely downloadable research corpus per project documentation
- **Rights/access notes:** Check dataset licence and attribution before redistribution
- **Specific linguistic coverage:** Speech-to-standard correspondences, Swiss discourse and pronunciation context
- **Main limitation:** Dialect-heavy audio; not pure Germany Standard German
- **Recommended scope:** Acquire as a labeled CH supplement only
- **Command/download hint:** `manual: follow project download instructions`

## common_voice_de_scripted — Mozilla Common Voice German Scripted Speech

- **Priority:** Tier 1
- **Direct link:** https://commonvoice.mozilla.org/en/datasets
- **Organization/author:** Mozilla Foundation / contributors
- **Category / genre:** speech corpus / read prompts with validated audio
- **Major topics:** broad short utterances; names; factual and practical statements
- **Register / CEFR:** neutral read speech / A1–B2
- **German variety / modality:** DACH-mixed German; metadata permits filtering / audio + sentence text
- **Format:** TSV metadata + MP3 clips in tar archives
- **Approximate usable material:** Large current release; tens of GB of audio, with validated_sentences.tsv
- **Access / availability:** bulk_open — Direct dataset download after selecting German/version
- **Rights/access notes:** Mozilla dataset terms and per-release licence; retain speaker and validation metadata
- **Specific linguistic coverage:** Short well-formed sentences, pronunciation, orthography and spoken reference
- **Main limitation:** Read speech rather than spontaneous dialogue; duplicates and odd prompts
- **Recommended scope:** Download sentence metadata first; audio only for a quality-controlled subset or TTS validation
- **Command/download hint:** `manual download; tools/acquire.py records destination`

## opensubtitles_opus — OPUS OpenSubtitles German

- **Priority:** Tier 3
- **Direct link:** https://opus.nlpl.eu/OpenSubtitles/corpus/version/OpenSubtitles
- **Organization/author:** OPUS / subtitle contributors
- **Category / genre:** dialogue corpus / film and television subtitles
- **Major topics:** relationships; conflict; humor; daily interaction; crime; work; emotion
- **Register / CEFR:** informal spoken-like, genre-dependent / A1–C1
- **German variety / modality:** mixed translated/dubbed German; not reliably DE-native / subtitle dialogue
- **Format:** TMX/Moses/monolingual text via OPUS tools
- **Approximate usable material:** Very large—millions of subtitle lines
- **Access / availability:** bulk_open — Downloadable through OPUS/OpusTools
- **Rights/access notes:** Corpus-specific licensing/attribution; many texts are copyrighted derivatives—use as internal research/reference only
- **Specific linguistic coverage:** Conversational ellipsis, discourse particles, emotional language, questions and commands
- **Main limitation:** Translationese, fragments, timing splits, profanity, fictional skew, duplicates
- **Recommended scope:** Cap at 100K–300K high-quality complete sentences after deduplication and language-quality scoring
- **Command/download hint:** `opus_read -d OpenSubtitles -s de -t en -wm moses -w raw.de raw.en`

## europarl_opus — OPUS Europarl German

- **Priority:** Tier 2
- **Direct link:** https://opus.nlpl.eu/Europarl/corpus/version/Europarl
- **Organization/author:** European Parliament / OPUS
- **Category / genre:** institutional parallel corpus / parliamentary speeches
- **Major topics:** EU policy; economics; law; environment; international affairs
- **Register / CEFR:** formal spoken-to-written / B2–C1
- **German variety / modality:** EU German, largely Standard / spoken transcript / translated parallel text
- **Format:** TMX/Moses via OPUS
- **Approximate usable material:** Millions of aligned sentence pairs across languages
- **Access / availability:** bulk_open — OpusTools/direct packages
- **Rights/access notes:** Check Europarl/OPUS terms and cite corpus
- **Specific linguistic coverage:** Formal arguments, procedural language, polite disagreement, complex clauses
- **Main limitation:** Translationese and institutional repetition
- **Recommended scope:** Acquire German side; sample 100K–250K after deduplication
- **Command/download hint:** `opus_read -d Europarl -s de -t en -wm moses -w raw.de raw.en`

## dgt_opus — OPUS DGT Translation Memory

- **Priority:** Tier 2
- **Direct link:** https://opus.nlpl.eu/DGT/corpus/version/DGT
- **Organization/author:** European Commission DGT / OPUS
- **Category / genre:** legal/administrative parallel corpus / EU legislation and administrative translation
- **Major topics:** regulation; policy; institutions; procedures
- **Register / CEFR:** formal legal-administrative / C1
- **German variety / modality:** EU German Standard / written translated text
- **Format:** TMX/Moses via OPUS
- **Approximate usable material:** Very large aligned translation memory
- **Access / availability:** bulk_open — OpusTools/direct packages
- **Rights/access notes:** European Commission reuse terms plus OPUS metadata
- **Specific linguistic coverage:** Terminology consistency, legal collocations, modality, conditions
- **Main limitation:** Strong translationese and formulaicity
- **Recommended scope:** Sample narrowly by document and lexical need; do not let it dominate
- **Command/download hint:** `opus_read -d DGT -s de -t en -wm moses -w raw.de raw.en`

## jrc_acquis_opus — OPUS JRC-Acquis German

- **Priority:** Tier 3
- **Direct link:** https://opus.nlpl.eu/JRC-Acquis/corpus/version/JRC-Acquis
- **Organization/author:** European Commission Joint Research Centre / OPUS
- **Category / genre:** legal parallel corpus / EU acquis
- **Major topics:** law; regulation; institutions
- **Register / CEFR:** formal legal / C1
- **German variety / modality:** EU German Standard / written translated text
- **Format:** TMX/Moses via OPUS
- **Approximate usable material:** Large aligned legal collection
- **Access / availability:** bulk_open — OpusTools/direct packages
- **Rights/access notes:** Follow JRC/OPUS terms
- **Specific linguistic coverage:** Legal phraseology and long conditional constructions
- **Main limitation:** Older and highly formulaic; overlaps DGT
- **Recommended scope:** Use only to fill legal collocation gaps not covered by current German statutes
- **Command/download hint:** `opus_read -d JRC-Acquis -s de -t en -wm moses -w raw.de raw.en`

## emea_opus — OPUS EMEA German

- **Priority:** Tier 2
- **Direct link:** https://opus.nlpl.eu/EMEA/corpus/version/EMEA
- **Organization/author:** European Medicines Agency source documents / OPUS
- **Category / genre:** medical-regulatory parallel corpus / medication; indications; contraindications; dosage; adverse effects
- **Major topics:** formal technical/regulatory
- **Register / CEFR:** B2–C1 / EU German Standard
- **German variety / modality:** written translated text / TMX/Moses via OPUS
- **Format:** Hundreds of thousands of aligned segments depending version
- **Approximate usable material:** bulk_open
- **Access / availability:** OpusTools/direct packages — Check source-document and OPUS terms
- **Rights/access notes:** Medical collocations, warnings, passive voice, dosage and risk language
- **Specific linguistic coverage:** Translationese and repetitive templates
- **Main limitation:** Acquire and retain 20K–50K diverse complete sentences
- **Recommended scope:** opus_read -d EMEA -s de -t en -wm moses -w raw.de raw.en
- **Command/download hint:** manual acquisition

## ted2020_opus — OPUS TED2020 German

- **Priority:** Tier 2
- **Direct link:** https://opus.nlpl.eu/TED2020/corpus/version/TED2020
- **Organization/author:** TED / OPUS
- **Category / genre:** talk transcript corpus / science; society; personal stories; technology; ideas
- **Major topics:** semi-formal spoken, narrative/explanatory
- **Register / CEFR:** B1–C1 / international German translation/subtitles
- **German variety / modality:** spoken transcript / subtitles / TMX/Moses via OPUS
- **Format:** Large multi-topic aligned transcript corpus
- **Approximate usable material:** bulk_open
- **Access / availability:** OpusTools/direct packages — TED/OPUS reuse conditions; internal reference recommended
- **Rights/access notes:** Storytelling, explanations, rhetorical questions, examples, audience address
- **Specific linguistic coverage:** Mostly translated subtitles and segmentation artifacts
- **Main limitation:** Acquire 50K–100K high-confidence complete sentences
- **Recommended scope:** opus_read -d TED2020 -s de -t en -wm moses -w raw.de raw.en
- **Command/download hint:** manual acquisition

## qed_opus — OPUS QED German

- **Priority:** Tier 3
- **Direct link:** https://opus.nlpl.eu/QED/corpus/version/QED
- **Organization/author:** Educational video contributors / OPUS
- **Category / genre:** educational transcript corpus / tutorials; lectures; explanations; practical skills
- **Major topics:** instructional spoken
- **Register / CEFR:** B1–C1 / translated Standard German
- **German variety / modality:** spoken transcript / subtitles / TMX/Moses via OPUS
- **Format:** Large multi-domain educational collection
- **Approximate usable material:** bulk_open
- **Access / availability:** OpusTools/direct packages — Corpus-specific terms; internal reference recommended
- **Rights/access notes:** Procedures, causal explanation, definitions, demonstrations
- **Specific linguistic coverage:** Translationese, subtitle fragments, uneven quality
- **Main limitation:** Use a 25K–50K filtered sample for instructional language
- **Recommended scope:** opus_read -d QED -s de -t en -wm moses -w raw.de raw.en
- **Command/download hint:** manual acquisition

## gnome_opus — OPUS GNOME localization corpus

- **Priority:** Tier 2
- **Direct link:** https://opus.nlpl.eu/GNOME/corpus/version/GNOME
- **Organization/author:** GNOME localization teams / OPUS
- **Category / genre:** software localization corpus / desktop software; settings; errors; actions; accessibility
- **Major topics:** concise technical UI
- **Register / CEFR:** A2–B2 / Standard German localization
- **German variety / modality:** written UI strings / TMX/Moses via OPUS
- **Format:** Tens of thousands of localized segments
- **Approximate usable material:** bulk_open
- **Access / availability:** OpusTools/direct packages — Open-source project licences; retain project attribution
- **Rights/access notes:** Commands, labels, error messages, user actions, technical collocations
- **Specific linguistic coverage:** Fragments and placeholders; not ordinary prose
- **Main limitation:** Keep only sentence-like strings and high-value UI messages
- **Recommended scope:** opus_read -d GNOME -s de -t en -wm moses -w raw.de raw.en
- **Command/download hint:** manual acquisition

## kde4_opus — OPUS KDE4 localization corpus

- **Priority:** Tier 2
- **Direct link:** https://opus.nlpl.eu/KDE4/corpus/version/KDE4
- **Organization/author:** KDE localization teams / OPUS
- **Category / genre:** software localization corpus / desktop software; files; networking; settings; support
- **Major topics:** concise technical UI
- **Register / CEFR:** A2–B2 / Standard German localization
- **German variety / modality:** written UI strings / TMX/Moses via OPUS
- **Format:** Large localized-string corpus
- **Approximate usable material:** bulk_open
- **Access / availability:** OpusTools/direct packages — Open-source project licences; retain project attribution
- **Rights/access notes:** Technology vocabulary, imperative/help language, warnings
- **Specific linguistic coverage:** Fragments, variables, duplication, translationese
- **Main limitation:** Keep 10K–30K sentence-like strings after placeholder filtering
- **Recommended scope:** opus_read -d KDE4 -s de -t en -wm moses -w raw.de raw.en
- **Command/download hint:** manual acquisition

## deplain — DEPlain

- **Priority:** Tier 1
- **Direct link:** https://github.com/rstodden/DEPlain
- **Organization/author:** Regina Stodden, Omar Momen, Laura Kallmeyer
- **Category / genre:** plain-language aligned corpus / professionally simplified news/web documents
- **Major topics:** news; public information; society
- **Register / CEFR:** neutral standard and plain language paired / A2–C1
- **German variety / modality:** Germany Standard German / written aligned text
- **Format:** repository datasets/code; document and sentence alignments
- **Approximate usable material:** DEplain-APA: 483 document pairs, 25,607 original sentences and 13,122 manually aligned sentence pairs; additional web material
- **Access / availability:** bulk_mixed — Git repository; some subcorpora available on request
- **Rights/access notes:** Licences differ by subcorpus; follow README and source rights
- **Specific linguistic coverage:** Register/complexity contrast, paraphrase, lexical and syntactic alternatives
- **Main limitation:** Some data request-only; limited domains; pairs may duplicate semantics
- **Recommended scope:** Clone repository immediately; ingest available licensed sentence pairs with complexity labels
- **Command/download hint:** `python tools/acquire.py fetch deplain`

## simple_german_corpus — A New Aligned Simple German Corpus

- **Priority:** Tier 1
- **Direct link:** https://github.com/buschmo/Simple-German-Corpus
- **Organization/author:** Vanessa Toborek et al.
- **Category / genre:** plain-language aligned corpus / standard/simple parallel web documents
- **Major topics:** public information; accessibility; society
- **Register / CEFR:** neutral and controlled simple language / A2–C1
- **German variety / modality:** Germany Standard German / written aligned text
- **Format:** Git repository with crawler, matching code and results workflow
- **Approximate usable material:** Hundreds of aligned/comparable documents; exact current output depends on archived sources
- **Access / availability:** bulk_open_code — Code/data repository; crawler uses archived websites
- **Rights/access notes:** MIT code licence; individual crawled texts retain source rights
- **Specific linguistic coverage:** CEFR/register leveling, sentence splitting, syntactic simplification contrasts
- **Main limitation:** Source copyright and crawler reproducibility; simple-language conventions can be unnatural for general learners
- **Recommended scope:** Clone code/data; use released results and metadata before recrawling
- **Command/download hint:** `python tools/acquire.py fetch simple_german_corpus`

## dwie — DWIE – Deutsche Welle Information Extraction corpus

- **Priority:** Tier 1
- **Direct link:** https://github.com/klimzaporojets/DWIE
- **Organization/author:** Klim Zaporojets et al.
- **Category / genre:** annotated news corpus / Deutsche Welle news articles
- **Major topics:** international news; politics; society; economy
- **Register / CEFR:** edited journalistic / B2–C1
- **German variety / modality:** Germany/international Standard German / written
- **Format:** JSON/document-level annotations
- **Approximate usable material:** Moderate document corpus with rich entity, coreference, relation and linking annotations
- **Access / availability:** bulk_open — GitHub and dataset mirrors
- **Rights/access notes:** Follow repository dataset licence and citation requirements
- **Specific linguistic coverage:** Coherent multi-sentence articles, entity chains, coreference, reporting structures
- **Main limitation:** News and named-entity heavy; not large enough as sole news source
- **Recommended scope:** Clone entire corpus; preserve document boundaries and annotations
- **Command/download hint:** `python tools/acquire.py fetch dwie`

## potec — PoTeC – Potsdam Textbook Corpus

- **Priority:** Tier 2
- **Direct link:** https://github.com/DiLi-Lab/PoTeC
- **Organization/author:** DiLi Lab / University of Potsdam and collaborators
- **Category / genre:** scientific/educational corpus / textbook excerpts
- **Major topics:** physics; biology
- **Register / CEFR:** formal explanatory academic / B2–C1
- **German variety / modality:** Germany Standard German / written + reading data
- **Format:** text and linguistic/eye-tracking annotations; large files via OSF
- **Approximate usable material:** 12 scientific texts read by 75 participants
- **Access / availability:** bulk_open — GitHub plus OSF data
- **Rights/access notes:** Open research materials; follow repository/OSF licence
- **Specific linguistic coverage:** Scientific explanation, technical noun phrases, causation and process descriptions
- **Main limitation:** Tiny text volume and narrow domains
- **Recommended scope:** Acquire all text; use as a high-quality scientific style anchor, not volume source
- **Command/download hint:** `python tools/acquire.py fetch potec`

## ggponc — GGPONC 2.0 – German oncology guideline corpus

- **Priority:** Tier 3
- **Direct link:** https://zenodo.org/records/12518458
- **Organization/author:** German Guideline Program in Oncology / research consortium
- **Category / genre:** medical guideline corpus / clinical practice guidelines
- **Major topics:** oncology; diagnosis; therapy; evidence; recommendations
- **Register / CEFR:** formal expert medical / C1
- **German variety / modality:** Germany medical Standard German / written annotated text
- **Format:** XML/annotated research corpus
- **Approximate usable material:** One of the largest German medical guideline corpora; exact release files on Zenodo
- **Access / availability:** restricted_request — Access request through Zenodo/community
- **Rights/access notes:** Non-commercial research and no redistribution restrictions apply to some releases; each user may need individual access
- **Specific linguistic coverage:** Medical terminology, evidence levels, recommendations, ellipsis in coordinated noun phrases
- **Main limitation:** Access/licence constraints and highly specialized content
- **Recommended scope:** Request only if project use qualifies; store outside Git and record restrictions
- **Command/download hint:** `manual: request access; never redistribute blindly`

## plainmedscale — PlainMedScale

- **Priority:** Tier 2
- **Direct link:** https://github.com/GS-Uni-Heidelberg/PlainMedScale
- **Organization/author:** Heidelberg University researchers
- **Category / genre:** multi-register medical corpus / topic-aligned medical explanations at four comprehensibility levels
- **Major topics:** diseases; symptoms; diagnosis; treatment; patient information
- **Register / CEFR:** expert, consumer, plain and accessible registers / A2–C1
- **German variety / modality:** German Standard German / written aligned/comparable text
- **Format:** GitHub + Zenodo
- **Approximate usable material:** Four-level topic-aligned German/English medical corpus; released August 2026
- **Access / availability:** bulk_open_or_mixed — Code and data links provided by authors
- **Rights/access notes:** New release: verify Zenodo licence and source-text conditions before redistribution
- **Specific linguistic coverage:** Exceptional register gradient, expert–lay paraphrases and patient-facing language
- **Main limitation:** Very new; source mix includes texts with differing rights; needs licence review
- **Recommended scope:** Acquire metadata/code now, data after licence check; label each level/source
- **Command/download hint:** `python tools/acquire.py fetch plainmedscale`

## textgrid — TextGrid Digital Library text corpus

- **Priority:** Tier 3
- **Direct link:** https://textgridrep.org/
- **Organization/author:** TextGrid / Göttingen State and University Library consortium
- **Category / genre:** literary/historical corpus / digitized German literature and cultural texts
- **Major topics:** fiction; drama; poetry; philosophy; history
- **Register / CEFR:** literary, often historical / C1
- **German variety / modality:** historical German and older Standard varieties / written
- **Format:** XML/TEI and full text corpus archives
- **Approximate usable material:** Text corpus downloads around 390 MB; over 120,000 works/items in repository holdings
- **Access / availability:** bulk_open — Whole-stock text corpus archives are downloadable
- **Rights/access notes:** Public-domain texts; repository metadata commonly CC BY; preserve attribution
- **Specific linguistic coverage:** Narrative, dialogue, description, emotion, stylistic range and literary syntax
- **Main limitation:** Mostly pre-20th-century; archaic lexicon/orthography can contaminate contemporary examples
- **Recommended scope:** Take a small curated 1–2% modern-compatible slice; tag year and never treat as everyday usage
- **Command/download hint:** `manual download from TextGrid repository`

## dw_nicos_weg — DW Learn German – Nicos Weg

- **Priority:** Tier 1
- **Direct link:** https://learngerman.dw.com/de/nicos-weg/c-36519687
- **Organization/author:** Deutsche Welle
- **Category / genre:** native-reviewed learner corpus / serial drama, exercises and lesson transcripts
- **Major topics:** introductions; housing; travel; family; work; services; relationships
- **Register / CEFR:** natural learner-oriented spoken / A1–B1
- **German variety / modality:** Germany Standard German / video/audio + transcript
- **Format:** web lessons; downloadable manuscripts/vocabulary PDFs for many units
- **Approximate usable material:** Hundreds of lesson scenes/exercises across A1–B1
- **Access / availability:** downloadable_manual — Manuscript/vocabulary PDFs available by lesson/course pages
- **Rights/access notes:** DW usage terms; internal educational reference; do not bulk mirror without checking terms
- **Specific linguistic coverage:** Natural progression, everyday dialogue, separable verbs, cases, word order, discourse particles
- **Main limitation:** Learner-scripted and recurring cast/topics; not enough advanced language
- **Recommended scope:** Download all official manuscripts and vocabulary PDFs first; keep lesson/level metadata
- **Command/download hint:** `manual: save official PDFs per lesson`

## dw_top_thema — DW Learn German – Top-Thema mit Vokabeln

- **Priority:** Tier 1
- **Direct link:** https://learngerman.dw.com/de/top-thema/s-55861562
- **Organization/author:** Deutsche Welle
- **Category / genre:** native-reviewed learner/news corpus / short current-affairs articles with audio/vocabulary
- **Major topics:** news; society; culture; science; economy
- **Register / CEFR:** edited accessible journalistic / B1
- **German variety / modality:** Germany Standard German / written + audio
- **Format:** web article, audio, manuscript/exercise/vocabulary PDFs on many entries
- **Approximate usable material:** Multi-year archive with many hundreds of units
- **Access / availability:** downloadable_manual — Individual pages and PDFs/audio
- **Rights/access notes:** DW terms; retain title/date/level and use internally unless redistribution is permitted
- **Specific linguistic coverage:** B1 news syntax, topical vocabulary, concise explanations, collocations
- **Main limitation:** Topic recency and news concentration; repeated exercise templates
- **Recommended scope:** Acquire 300–500 diverse units across years/topics, preserving article text and vocab notes
- **Command/download hint:** `manual or respectful page/PDF downloader after terms review`

## dw_video_thema — DW Learn German – Video-Thema

- **Priority:** Tier 1
- **Direct link:** https://learngerman.dw.com/de/video-thema/s-55861568
- **Organization/author:** Deutsche Welle
- **Category / genre:** native-reviewed audiovisual learner corpus / short documentary/report videos with transcripts and exercises
- **Major topics:** work; society; culture; technology; environment; people
- **Register / CEFR:** neutral spoken/reportage / B2
- **German variety / modality:** Germany Standard German / video/audio + transcript
- **Format:** web video, manuscript and worksheet PDFs
- **Approximate usable material:** Large multi-year archive with hundreds of units
- **Access / availability:** downloadable_manual — Transcripts/manuscripts and exercises commonly downloadable
- **Rights/access notes:** DW terms; internal reference unless explicit reuse allows more
- **Specific linguistic coverage:** Spoken reportage, interviews, B2 phrasing, connected speech, explanation
- **Main limitation:** Some voice-over/reportage rather than spontaneous dialogue
- **Recommended scope:** Acquire 200–400 topic-diverse units; preserve speaker distinctions when available
- **Command/download hint:** `manual or respectful page/PDF downloader after terms review`

## dw_slow_news — DW Langsam gesprochene Nachrichten

- **Priority:** Tier 1
- **Direct link:** https://learngerman.dw.com/de/langsam-gesprochene-nachrichten/s-60040332
- **Organization/author:** Deutsche Welle
- **Category / genre:** news transcript/audio corpus / daily news read slowly
- **Major topics:** international politics; economics; society; conflict; science
- **Register / CEFR:** formal broadcast news / B2–C1
- **German variety / modality:** Germany broadcast Standard German / audio + exact text
- **Format:** web text and downloadable audio
- **Approximate usable material:** Daily archive; thousands of dated bulletins over time
- **Access / availability:** downloadable_manual — Text pages and audio downloads
- **Rights/access notes:** DW terms; preserve date and segment boundaries
- **Specific linguistic coverage:** Broadcast phrasing, reported speech, passive, tense variation, pronunciation alignment
- **Main limitation:** International/political skew and repeated news formulas
- **Recommended scope:** Acquire a stratified 1–2 year sample, not every bulletin
- **Command/download hint:** `manual or RSS/page collector after terms review`

## dw_alltagsdeutsch — DW Alltagsdeutsch / Sprachbar

- **Priority:** Tier 2
- **Direct link:** https://learngerman.dw.com/de/alltagsdeutsch/s-56744441
- **Organization/author:** Deutsche Welle
- **Category / genre:** advanced learner/culture corpus / audio features and language columns
- **Major topics:** idioms; culture; social life; language; institutions
- **Register / CEFR:** neutral to informal, stylistically rich / C1
- **German variety / modality:** Germany Standard German / audio + transcript
- **Format:** web text/audio; worksheets on many entries
- **Approximate usable material:** Large archive of feature-length units
- **Access / availability:** downloadable_manual — Individual transcript/manuscript pages
- **Rights/access notes:** DW terms; preserve series, date and topic
- **Specific linguistic coverage:** Idioms, figurative language, register, wordplay, discourse and cultural references
- **Main limitation:** Advanced and feature-journalism skew
- **Recommended scope:** Acquire 150–300 units selected for lexical/functional diversity
- **Command/download hint:** `manual download after terms review`

## goethe_uebungen — Goethe-Institut – Deutsch üben / free practice materials

- **Priority:** Tier 1
- **Direct link:** https://www.goethe.de/de/spr/ueb.html
- **Organization/author:** Goethe-Institut
- **Category / genre:** native-reviewed learner corpus / interactive exercises, videos, readings and workplace/everyday modules
- **Major topics:** daily life; work; travel; culture; communication
- **Register / CEFR:** learner-oriented, natural neutral/informal/formal / A1–C2 (select A1–C1)
- **German variety / modality:** Germany Standard German with DACH cultural content / mixed written/spoken
- **Format:** web exercises, video/audio, some PDFs/apps
- **Approximate usable material:** Hundreds of free resources; some paid courses contain far more
- **Access / availability:** downloadable_manual — Some resources downloadable; many interactive only
- **Rights/access notes:** Goethe terms; use as reference and only download where offered
- **Specific linguistic coverage:** Controlled CEFR examples, communicative functions, grammar, pragmatic appropriateness
- **Main limitation:** Interactive content may be difficult to export; learner-domain concentration
- **Recommended scope:** Inventory and manually download offered PDFs/transcripts, prioritizing professional and B2–C1 materials
- **Command/download hint:** `manual inventory; no blind site mirroring`

## goethe_mein_weg — Goethe-Institut – Mein Weg nach Deutschland

- **Priority:** Tier 1
- **Direct link:** https://www.goethe.de/prj/mwd/de/
- **Organization/author:** Goethe-Institut
- **Category / genre:** integration/practical learner corpus / videos, texts and practical information
- **Major topics:** arrival; housing; work; offices; school; health; money; daily life
- **Register / CEFR:** accessible practical neutral / A1–B1
- **German variety / modality:** Germany Standard German / mixed written/spoken
- **Format:** web, video, exercises and practical text
- **Approximate usable material:** Dozens of topic modules with recurring characters and real-life information
- **Access / availability:** downloadable_manual — Web/video; selected materials may be downloadable
- **Rights/access notes:** Goethe terms; internal reference
- **Specific linguistic coverage:** Immigration/integration interactions, public offices, forms, housing and workplace pragmatics
- **Main limitation:** Learner-scripted; narrower target audience
- **Recommended scope:** Acquire complete topic inventory and offered transcripts/materials
- **Command/download hint:** `manual inventory`

## vhs_lernportal_general — vhs-Lernportal – Deutsch A1–C1

- **Priority:** Tier 1
- **Direct link:** https://www.vhs-lernportal.de/
- **Organization/author:** Deutscher Volkshochschul-Verband
- **Category / genre:** native-reviewed learner corpus / online courses and apps
- **Major topics:** daily life; family; shopping; housing; services; education; society
- **Register / CEFR:** practical learner-oriented / A1–C1
- **German variety / modality:** Germany Standard German / mixed written/spoken
- **Format:** interactive platform, apps, downloadable supplemental materials
- **Approximate usable material:** Large course system with thousands of exercises across levels
- **Access / availability:** downloadable_mixed — Free registration; apps/offline use and downloadable extras
- **Rights/access notes:** Platform terms; do not scrape authenticated content without permission
- **Specific linguistic coverage:** Broad CEFR-balanced daily and civic vocabulary; structured progression
- **Main limitation:** Interactive/authenticated content; exercise repetition
- **Recommended scope:** Download public supplemental PDFs and app/offline packages where allowed; use platform manually for gaps
- **Command/download hint:** `manual/account-based`

## vhs_beruf — vhs-Lernportal – Deutsch für den Beruf A2–C1

- **Priority:** Tier 1
- **Direct link:** https://www.vhs-lernportal.de/wws/deutsch-fuer-den-beruf.php
- **Organization/author:** Deutscher Volkshochschul-Verband
- **Category / genre:** professional learner corpus / occupation-oriented courses
- **Major topics:** applications; meetings; schedules; customer service; safety; healthcare; trades; office communication
- **Register / CEFR:** neutral/formal workplace with spoken interaction / A2–C1
- **German variety / modality:** Germany Standard German / mixed written/spoken
- **Format:** interactive courses, apps and supplemental downloads
- **Approximate usable material:** Multiple large vocational courses and thousands of exercises
- **Access / availability:** downloadable_mixed — Free account; some material downloadable/offline
- **Rights/access notes:** Platform terms; do not bulk scrape authenticated content
- **Specific linguistic coverage:** Workplace emails, procedures, role-specific interactions, polite disagreement, instructions
- **Main limitation:** Exercise/platform structure; not a raw corpus
- **Recommended scope:** Prioritize public/downloadable B2–C1 vocational supplements and manually curate authentic dialogues/emails
- **Command/download hint:** `manual/account-based`

## nachrichtenleicht — Nachrichtenleicht

- **Priority:** Tier 1
- **Direct link:** https://www.nachrichtenleicht.de/
- **Organization/author:** Deutschlandfunk
- **Category / genre:** easy-news corpus / news in simple language with audio
- **Major topics:** politics; economy; society; culture; sports
- **Register / CEFR:** clear edited news / A2–B1
- **German variety / modality:** Germany Standard German / written + audio
- **Format:** web articles, RSS and downloadable audio
- **Approximate usable material:** Large ongoing archive with multiple items weekly
- **Access / availability:** downloadable_manual — RSS, article pages and audio downloads
- **Rights/access notes:** Deutschlandradio terms; internal reference and metadata retention
- **Specific linguistic coverage:** Simple but authentic news paraphrase, short clauses, explanation of public vocabulary
- **Main limitation:** Controlled simplification may overuse short sentences and explicit nouns
- **Recommended scope:** Acquire a topic-balanced 2–3 year article sample with audio metadata
- **Command/download hint:** `RSS/page collector after terms review`

## bamf_willkommen — BAMF – Willkommen in Deutschland

- **Priority:** Tier 1
- **Direct link:** https://www.bamf.de/SharedDocs/Anlagen/DE/Integration/WillkommenDeutschland/willkommen-in-deutschland.html
- **Organization/author:** Federal Office for Migration and Refugees (BAMF)
- **Category / genre:** official practical/integration corpus / orientation handbook
- **Major topics:** housing; work; school; health; money; government; rights; daily life
- **Register / CEFR:** accessible official practical / A2–B2
- **German variety / modality:** Germany Standard German / written
- **Format:** HTML/PDF, often multilingual and accessible versions
- **Approximate usable material:** One substantial handbook plus related modules
- **Access / availability:** bulk_manual — Official PDF downloads
- **Rights/access notes:** Official publication; check imprint/reuse terms and retain edition
- **Specific linguistic coverage:** Real-world civic vocabulary, procedures, modal verbs, explanations, addresses to reader
- **Main limitation:** Single-document topic structure; some migration-specific context
- **Recommended scope:** Download current German PDF and accessible/simple variants; sentence-split with section metadata
- **Command/download hint:** `manual direct PDF`

## bamf_leben_in_deutschland — BAMF – Leben in Deutschland question catalog

- **Priority:** Tier 2
- **Direct link:** https://www.bamf.de/SharedDocs/Anlagen/DE/Integration/Einbuergerung/gesamtfragenkatalog-lebenindeutschland.html
- **Organization/author:** BAMF
- **Category / genre:** official civic/assessment corpus / citizenship and integration questions
- **Major topics:** constitution; history; politics; rights; federal states; society
- **Register / CEFR:** accessible official question style / A2–B2
- **German variety / modality:** Germany Standard German / written
- **Format:** PDF question catalogs
- **Approximate usable material:** 300 nationwide questions plus 160 state-specific questions
- **Access / availability:** bulk_manual — Official PDF download
- **Rights/access notes:** Official publication; retain version/date
- **Specific linguistic coverage:** Question structures, civic vocabulary, answer options and factual formulations
- **Main limitation:** Multiple-choice format and limited sentence diversity
- **Recommended scope:** Acquire full catalog but down-weight repeated templates
- **Command/download hint:** `manual direct PDF`

## berufenet — BERUFENET

- **Priority:** Tier 1
- **Direct link:** https://web.arbeitsagentur.de/berufenet/
- **Organization/author:** Federal Employment Agency
- **Category / genre:** official occupational corpus / occupation profiles and task descriptions
- **Major topics:** careers; skills; training; tools; work conditions; industries
- **Register / CEFR:** neutral formal practical / B1–C1
- **German variety / modality:** Germany Standard German / written
- **Format:** web database with structured occupation pages
- **Approximate usable material:** Very large: hundreds of detailed occupation profiles and related fields
- **Access / availability:** web_reference — Public web database; no simple full dump identified
- **Rights/access notes:** Respect site terms/robots; store links/metadata or manually exported pages unless permission exists
- **Specific linguistic coverage:** Occupation-specific verbs/nouns, task descriptions, qualifications, safety and work settings
- **Main limitation:** Potential anti-scraping/terms constraints; many noun phrases and lists
- **Recommended scope:** Start with 100–200 representative occupations across sectors; manual/export or permitted API only
- **Command/download hint:** `manual inventory/export`

## bundesportal — Federal Administration Portal – Verwaltungsportal Bund

- **Priority:** Tier 1
- **Direct link:** https://verwaltung.bund.de/portal/DE/
- **Organization/author:** Federal Ministry of the Interior and public administrations
- **Category / genre:** official administrative corpus / service descriptions and procedures
- **Major topics:** registration; permits; taxes; documents; family; vehicles; business; benefits
- **Register / CEFR:** formal practical administrative / B1–C1
- **German variety / modality:** Germany Standard German / written
- **Format:** structured web pages
- **Approximate usable material:** Thousands of service descriptions across federal/state/local administration
- **Access / availability:** web_reference — Public pages; structured navigation, no universal dump assumed
- **Rights/access notes:** Respect portal terms/robots and preserve jurisdiction/date
- **Specific linguistic coverage:** Forms, prerequisites, deadlines, documents, fees, conditional and procedural language
- **Main limitation:** Template repetition; jurisdiction-specific variants; scraping constraints
- **Recommended scope:** Sample 300–500 services across life situations and regions, deduplicating template text
- **Command/download hint:** `manual/permitted crawler`

## verbraucherzentrale — Verbraucherzentrale information and Musterbriefe

- **Priority:** Tier 1
- **Direct link:** https://www.verbraucherzentrale.de/musterbriefe
- **Organization/author:** German consumer centres
- **Category / genre:** consumer/practical corpus / advice articles, complaints and model letters
- **Major topics:** contracts; purchases; banking; telecoms; energy; travel; refunds; scams
- **Register / CEFR:** neutral advice plus formal correspondence / B1–C1
- **German variety / modality:** Germany Standard German / written
- **Format:** HTML, downloadable model-letter files/PDFs
- **Approximate usable material:** Large advice site plus many reusable letter templates
- **Access / availability:** downloadable_manual — Model letters and articles available individually
- **Rights/access notes:** Terms vary; model letters intended for consumer use, but preserve source and do not republish wholesale without checking
- **Specific linguistic coverage:** Complaints, requests, deadlines, cancellation, negotiation, customer-service and legal-practical collocations
- **Main limitation:** Template formulaicity and legal topic skew
- **Recommended scope:** Acquire all clearly downloadable model letters and a balanced sample of advice articles
- **Command/download hint:** `manual direct downloads`

## gesund_bund — gesund.bund.de – Diseases A–Z and health information

- **Priority:** Tier 1
- **Direct link:** https://gesund.bund.de/krankheiten
- **Organization/author:** Federal Ministry of Health service
- **Category / genre:** official patient-information corpus / disease and health explanations
- **Major topics:** symptoms; causes; diagnosis; treatment; prevention; care
- **Register / CEFR:** clear neutral medical/consumer / B1–C1
- **German variety / modality:** Germany Standard German / written
- **Format:** structured HTML; some media
- **Approximate usable material:** Large A–Z collection with many detailed pages
- **Access / availability:** web_reference — Public pages; no complete bulk dump identified
- **Rights/access notes:** Respect site terms/robots; preserve medical review/update metadata
- **Specific linguistic coverage:** Patient-facing medical collocations, explanations, uncertainty, advice and care pathways
- **Main limitation:** Topic concentration; lengthy page boilerplate
- **Recommended scope:** Acquire 100–200 diverse condition pages only through permitted means; keep section labels
- **Command/download hint:** `manual/permitted crawler`

## rki_ratgeber — RKI-Ratgeber

- **Priority:** Tier 2
- **Direct link:** https://www.rki.de/ratgeber
- **Organization/author:** Robert Koch Institute
- **Category / genre:** public-health expert corpus / professional infectious-disease guidance
- **Major topics:** epidemiology; transmission; diagnosis; prevention; reporting; hygiene
- **Register / CEFR:** formal technical medical/public health / C1
- **German variety / modality:** Germany Standard German / written
- **Format:** HTML and linked PDFs
- **Approximate usable material:** Dozens of detailed disease guides, updated individually
- **Access / availability:** downloadable_manual — Web/PDF pages
- **Rights/access notes:** Official guidance; retain update date and citation
- **Specific linguistic coverage:** Technical causation, risk, surveillance, recommendation and passive constructions
- **Main limitation:** Specialized and institutionally formulaic
- **Recommended scope:** Acquire all current Ratgeber documents but cap total influence; retain section/date metadata
- **Command/download hint:** `manual link collector`

## uba_publications — Umweltbundesamt publications

- **Priority:** Tier 2
- **Direct link:** https://www.umweltbundesamt.de/publikationen
- **Organization/author:** German Environment Agency
- **Category / genre:** scientific/official corpus / reports, guidance and studies
- **Major topics:** climate; air; water; chemicals; waste; transport; health; agriculture; procurement
- **Register / CEFR:** formal technical and public-facing / B2–C1
- **German variety / modality:** Germany Standard German / written
- **Format:** HTML metadata + downloadable PDFs
- **Approximate usable material:** Thousands of publications over many years
- **Access / availability:** downloadable_manual — PDFs from publication pages
- **Rights/access notes:** Per-document reuse/licence may vary; retain report metadata and only redistribute when allowed
- **Specific linguistic coverage:** Environmental/scientific vocabulary, measurements, uncertainty, methods, policy recommendations
- **Main limitation:** PDF extraction issues, very long documents, bureaucratic style
- **Recommended scope:** Acquire 30–60 recent reports spanning topics and audience levels; extract executive summaries and prose sections
- **Command/download hint:** `manual PDF downloader`

## destatis_press — Destatis press releases

- **Priority:** Tier 1
- **Direct link:** https://www.destatis.de/DE/Presse/_inhalt.html
- **Organization/author:** Federal Statistical Office
- **Category / genre:** official statistical/news corpus / press releases and statistical explanations
- **Major topics:** population; prices; labor; trade; education; health; economy; environment
- **Register / CEFR:** formal concise explanatory / B2–C1
- **German variety / modality:** Germany Standard German / written
- **Format:** HTML; tables and linked files
- **Approximate usable material:** Continuous archive with hundreds of releases per year
- **Access / availability:** web_reference — Public release pages; email service; no bulk text dump assumed
- **Rights/access notes:** Official content; preserve release number/date and source citation
- **Specific linguistic coverage:** Numbers, comparisons, trends, percentages, methodological hedges and reported findings
- **Main limitation:** Repetitive release formulas and numeric density
- **Recommended scope:** Acquire 300–500 releases across 3–5 years and all major topic departments
- **Command/download hint:** `RSS/page collector after terms review`

## ssoar — SSOAR – Social Science Open Access Repository

- **Priority:** Tier 2
- **Direct link:** https://www.gesis.org/ssoar
- **Organization/author:** GESIS – Leibniz Institute for the Social Sciences
- **Category / genre:** academic repository / papers, reports and working papers
- **Major topics:** sociology; politics; media; migration; inequality; methods; culture
- **Register / CEFR:** academic formal / C1
- **German variety / modality:** Germany and broader DACH Standard German / written
- **Format:** PDF full texts + OAI-PMH metadata
- **Approximate usable material:** Large and continuously growing full-text repository
- **Access / availability:** downloadable_mixed — Freely accessible full texts; metadata harvestable via OAI-PMH
- **Rights/access notes:** Metadata CC0; each full text has its own licence/terms on cover page
- **Specific linguistic coverage:** Academic argument, methods, evidence, hedging, comparison and conclusions
- **Main limitation:** Many English texts, long PDFs, varied licences and OCR quality
- **Recommended scope:** Harvest metadata first; select 100–300 German, recent, openly licensed documents across subfields
- **Command/download hint:** `OAI metadata + licence-aware PDF fetch`

## pedocs — peDOCS

- **Priority:** Tier 2
- **Direct link:** https://www.pedocs.de/
- **Organization/author:** DIPF | Leibniz Institute for Research and Information in Education
- **Category / genre:** academic repository / education research full texts
- **Major topics:** schools; teaching; learning; higher education; policy; childhood; vocational education
- **Register / CEFR:** academic formal / C1
- **German variety / modality:** Germany/DACH Standard German / written
- **Format:** PDF full texts + repository metadata/OAI
- **Approximate usable material:** Large education-science open-access collection
- **Access / availability:** downloadable_mixed — Freely accessible full texts; repository metadata
- **Rights/access notes:** Licence varies by item; retain cover metadata and rights
- **Specific linguistic coverage:** Education/research terminology, literature review, argumentation and findings
- **Main limitation:** Long PDFs, older publications, mixed licences
- **Recommended scope:** Select 100–200 recent German OA papers/reports across education topics
- **Command/download hint:** `metadata-first, licence-aware downloads`

## gms — German Medical Science

- **Priority:** Tier 2
- **Direct link:** https://www.egms.de/
- **Organization/author:** German Association of the Scientific Medical Societies and partners
- **Category / genre:** academic medical repository / peer-reviewed articles, guidelines and conference material
- **Major topics:** medicine; healthcare; public health; clinical research
- **Register / CEFR:** academic/technical medical / C1
- **German variety / modality:** Germany Standard German; some English / written
- **Format:** HTML, PDF and often XML
- **Approximate usable material:** Large multi-journal open-access platform
- **Access / availability:** downloadable_mixed — Article-level HTML/PDF/XML where offered
- **Rights/access notes:** Open-access terms vary by journal/article; preserve licence and citation
- **Specific linguistic coverage:** Research abstracts, methods, outcomes, medical argument and formal terminology
- **Main limitation:** Many English articles and highly specialized text
- **Recommended scope:** Select German-language HTML/XML first; 50–150 documents across specialties
- **Command/download hint:** `manual/API-like article downloads`

## dwds_dereko_reference — DWDS and DeReKo/COSMAS II reference corpora

- **Priority:** Tier 3
- **Direct link:** https://www.dwds.de/
- **Organization/author:** Berlin-Brandenburg Academy / IDS Mannheim
- **Category / genre:** query/reference corpus / large balanced and monitor corpora
- **Major topics:** general language across genres and periods
- **Register / CEFR:** all registers depending subcorpus / A1–C1
- **German variety / modality:** Germany/DACH varieties by corpus / written and spoken query results
- **Format:** web corpus interfaces; some CLARIN downloads
- **Approximate usable material:** Billions of tokens queryable across DWDS/DeReKo collections
- **Access / availability:** query_only — Concordance/query access; most DeReKo text is not bulk downloadable
- **Rights/access notes:** Access and citation terms apply; do not scrape query services
- **Specific linguistic coverage:** Best source for validating collocations, case government, frequency, sense/register and diachrony
- **Main limitation:** Not a convenient repo corpus; copyright prevents bulk export
- **Recommended scope:** Use programmatically/manual queries during sentence review, not bulk ingestion
- **Command/download hint:** `reference only`

## swiss_text_corpus — Swiss Text Corpus

- **Priority:** Tier 3
- **Direct link:** https://www.chtk.ch/index.php/en/corpus-overview
- **Organization/author:** University of Basel / Swiss corpus partners
- **Category / genre:** regional reference corpus / balanced Swiss Standard German text
- **Major topics:** news; literature; nonfiction; practical and institutional texts
- **Register / CEFR:** mixed written registers / B1–C1
- **German variety / modality:** CH Standard German / written
- **Format:** corpus query/download access varies
- **Approximate usable material:** About 23.5 million words
- **Access / availability:** query_or_request — Corpus interface and project access; bulk availability depends on current terms
- **Rights/access notes:** Follow corpus licence/access terms
- **Specific linguistic coverage:** Swiss lexical, orthographic and institutional variants in balanced genres
- **Main limitation:** Regional and often query-only; possible older material
- **Recommended scope:** Use as CH validation and acquire only permitted exports/samples
- **Command/download hint:** `reference/query`

## austrian_media_corpus — Austrian Media Corpus

- **Priority:** Tier 3
- **Direct link:** https://www.oeaw.ac.at/acdh/research/language-resources/austrian-media-corpus
- **Organization/author:** Austrian Academy of Sciences / Austrian Press Agency
- **Category / genre:** regional reference corpus / Austrian journalistic prose
- **Major topics:** politics; society; economy; culture; sports
- **Register / CEFR:** edited journalistic / B1–C1
- **German variety / modality:** AT Standard German / written
- **Format:** corpus interface/research access
- **Approximate usable material:** Very large media corpus spanning the Austrian media landscape
- **Access / availability:** query_or_request — Research/query access; bulk rights constrained by source copyright
- **Rights/access notes:** Follow ACDH/APA access conditions
- **Specific linguistic coverage:** Austrian vocabulary, institutions, spelling and journalistic usage
- **Main limitation:** Copyright/access limits; genre concentrated in news
- **Recommended scope:** Use for AT validation and targeted concordance samples, not repo bulk
- **Command/download hint:** `reference/query`

## c4_dach — C4 – Corpus of Contemporary German in Germany, Austria, Switzerland and South Tyrol

- **Priority:** Tier 3
- **Direct link:** https://www.dwds.de/d/korpora/c4
- **Organization/author:** DWDS / partner institutions
- **Category / genre:** regional comparative reference corpus / contemporary DACH mixed corpus
- **Major topics:** general language by country/region
- **Register / CEFR:** mixed written / B1–C1
- **German variety / modality:** DE/AT/CH/South Tyrol labeled / written
- **Format:** DWDS corpus query
- **Approximate usable material:** Large federated contemporary corpus
- **Access / availability:** query_only — Queryable through DWDS; component download rights vary
- **Rights/access notes:** Follow DWDS/component terms
- **Specific linguistic coverage:** Direct comparison of regional lexical and grammatical preferences
- **Main limitation:** Not bulk downloadable as a unified open corpus
- **Recommended scope:** Use for regional validation and sense/register checks
- **Command/download hint:** `reference only`

## tagesschau_rss — tagesschau.de RSS and article archive

- **Priority:** Tier 2
- **Direct link:** https://www.tagesschau.de/infoservices/alle-meldungen-100.html
- **Organization/author:** ARD-aktuell
- **Category / genre:** public-broadcast news corpus / news articles, interviews and reports
- **Major topics:** Germany; world; economy; science; culture; regional news
- **Register / CEFR:** edited broadcast/web journalistic / B2–C1
- **German variety / modality:** Germany Standard German / written + some video/audio transcripts
- **Format:** HTML, RSS and media pages
- **Approximate usable material:** Large current archive and many topical feeds
- **Access / availability:** web_reference — RSS available; articles publicly readable
- **Rights/access notes:** Terms specify private/non-commercial constraints for feeds; do not mirror/redistribute indiscriminately
- **Specific linguistic coverage:** Current native journalism, quotations, interviews, analysis and regional reporting
- **Main limitation:** Copyright restrictions and heavy current-news/named-entity skew
- **Recommended scope:** Use RSS to build a metadata/link queue; manually retain small internal excerpts only where lawful
- **Command/download hint:** `RSS metadata only by default`

## dlf_podcasts — Deutschlandfunk podcast/audio archive

- **Priority:** Tier 3
- **Direct link:** https://www.deutschlandfunk.de/podcasts
- **Organization/author:** Deutschlandradio
- **Category / genre:** spoken journalism/culture reference / interviews, reports, discussions and features
- **Major topics:** politics; science; culture; society; history; media
- **Register / CEFR:** neutral/formal spontaneous and scripted spoken / B2–C1
- **German variety / modality:** Germany broadcast Standard German / audio; transcripts vary
- **Format:** MP3/podcast feeds; selected manuscripts
- **Approximate usable material:** Very large audio archive
- **Access / availability:** audio_reference — Audio downloads widely available; transcript availability inconsistent
- **Rights/access notes:** Deutschlandradio terms; do not assume transcript reuse
- **Specific linguistic coverage:** Spontaneous interview syntax, turn-taking, hedging, disagreement, pronunciation
- **Main limitation:** Many items lack transcripts; transcription would be machine-generated unless manually checked
- **Recommended scope:** Use only episodes with official manuscripts/transcripts or for audio validation
- **Command/download hint:** `manual transcript-only selection`
