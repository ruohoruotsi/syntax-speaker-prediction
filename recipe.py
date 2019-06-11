import prodigy
from prodigy.components.loaders import JSONL


@prodigy.recipe("audio-choice")
def audio_annotation(dataset, source):
    stream = JSONL(source)
    stream = add_options(stream)
    stream = list(stream)
    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "choice",
        "progress": progress,
    }

# {"html": "<audio controls autoplay loop><source src=\"http://localhost:9999/syntax131-0002.mp3\" type=\"audio/mp3\"></audio><p>Episode: 131, Second: 0002</p>",
# "text": "E131:S0002"}

def add_options(stream):
    """Helper function to add options to every task in a stream."""
    options = [
        {"id": "english", "text": "💬💬 English"},
        {"id": "other",   "text": "⛔️⛔️ Not-English"},
    ]
    for task in stream:
        task["options"] = options
        yield task


def progress(session_count, total):
    custom_progress = session_count / total
    return custom_progress
