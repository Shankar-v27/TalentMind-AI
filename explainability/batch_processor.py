# explainability/batch_processor.py


def create_batches(items, batch_size):

    batches = []

    for i in range(
        0,
        len(items),
        batch_size
    ):

        batches.append(
            items[i:i + batch_size]
        )

    return batches