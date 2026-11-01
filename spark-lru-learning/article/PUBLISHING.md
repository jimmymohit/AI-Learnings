# Publishing package

Open `medium-formatted.html` in a browser. Copy the rendered article below the blue notice into a Medium draft. Local HTML/CSS is a copy source; it is not a Medium theme or a direct publishing integration. Check headings, code blocks, and image placement after pasting, since the editor may change formatting.

Replace the final GitHub placeholder URL with your repository link before publishing.

## Upload images manually

The draft already includes each image at its intended location. If an image does not transfer, upload the matching file from `assets/` there:

| File | Placement |
|---|---|
| `01-cover.png` | Below the subtitle |
| `02-partition-flow.png` | In “Put the cache where the work happens” |
| `03-lru-sequence.png` | In “Why LRU fits this problem” |
| `04-rag-boundary.png` | In “Where this fits in RAG” |
| `05-lru-animation.gif` | Optional replacement for the static LRU sequence image |

The static diagrams are 1600 × 900 PNGs. The animation is 960 × 540 with five frames. Check animation playback in the destination editor and published preview; retain the static image if playback is unsuitable. Alt text is in the Markdown/HTML draft. All visuals are original diagrams generated for this project.

## Editorial choices

Recommended title: **Stop Paying Twice for the Same Vector: Spark Meets the LRU Cache**

Alternative: **Spark, AI, and the Vector You Shouldn’t Compute Twice**

Alternative: **Before You Scale Your AI Pipeline, Give Spark a Memory**

Subtitle: *How a small cache can remove repeated AI embedding calls—and why its location inside a Spark job matters.*

Suggested tags: Apache Spark, Artificial Intelligence, Python, Caching, Data Engineering.

“Paying twice” refers to repeated compute; this local Ollama example does not incur a per-request API bill. The article claims fewer calls, not a measured wall-clock speedup. The expected 10/8/6 counts follow from tracing the controlled inputs and were cross-checked with the partition logic using the test provider. Live inference remains unverified. Retrieval and full RAG are clearly marked as extensions.

## Source and rebuild

Edit `medium-draft.md`, then run `python3 render_article.py` from this folder to rebuild HTML. The renderer uses only the Python standard library. `build_assets.py` rebuilds diagrams and the GIF with Pillow; its default fonts use macOS Arial paths. Adapt those paths on other operating systems.

Primary references are linked in the article: the Spark 4.0.0 RDD guide and Ollama embedding API documentation. Runtime behavior and snippets are based on this repository's implementation.
