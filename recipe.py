import prodigy
from prodigy.components.loaders import JSONL


@prodigy.recipe("audio-choice",
                dataset=prodigy.recipe_args['dataset'],
                file_path=("Path to audio", "positional", None, str))
def audio_annotation(dataset, file_path):
    stream = JSONL(file_path)
    stream = add_options(stream)
    stream = list(stream)
    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "choice",
        "progress": progress,
        "on_exit": on_exit
    }

# {"html": "<audio controls autoplay loop><source src=\"http://localhost:9999/syntax131-0002.mp3\" type=\"audio/mp3\"></audio><p>Episode: 131, Second: 0002</p>",
# "text": "E131:S0002"}

def add_options(stream):
    """Helper function to add options to every task in a stream."""
    options = [
        {"id": "english",     "text": "💬💬 🇬🇧English"},
        {"id": "not-english", "text": "⛔️⛔️ Not-English"},
    ]
    for task in stream:
        task["options"] = options
        yield task


def progress(session_count, total):
    custom_progress = session_count / total
    return custom_progress


def get_count_by_option(examples, option):
    filtered = [eg for eg in examples if option in eg['accept']]
    return len(filtered)


def on_exit(controller):
    """Get all annotations in the dataset, filter out the accepted tasks,
    count them by the selected options and print the counts."""
    examples = controller.db.get_dataset(controller.dataset)
    examples = [eg for eg in examples if eg['answer'] == 'accept']
    for option in ("english", "not-english"):
        count = get_count_by_option(examples, option)
        print('Annotated {} {} examples'.format(count, option))