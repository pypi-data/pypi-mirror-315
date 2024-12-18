# Batch Processor Module

This module provides functionality for processing data in batches with options for progress tracking, retries, and saving results to a file. It includes a `BatchProcessor` class and a `batch_processor_decorator` for easy integration into your projects.

## Usage

### BatchProcessor Class

1. **Import the BatchProcessor:**

   ```python
   from batchprocessor import BatchProcessor
   ```

2. **Define a function to process each batch:**

   ```python
   def process_batch(batch):
       # Your processing logic here
       return {"processed": batch, "status": "success"}
   ```

3. **Initialize the BatchProcessor:**

   ```python
   processor = BatchProcessor(
       iterable=your_data,
       batch_size=5,
       progress=True,
       save_to_file="output.json",
       retries=2,
       retry_delay=1.0,
   )
   ```

4. **Process the batches:**

   ```python
   results = processor.process(process_batch)
   print("Final Results:", results)
   ```

### batch_processor_decorator

1. **Import the decorator:**

   ```python
   from batchprocessor import batch_processor_decorator
   ```

2. **Decorate your batch processing function:**

   ```python
   @batch_processor_decorator(
       batch_size=5,
       progress=True,
       save_to_file="output_decorator.json",
       retries=2,
       retry_delay=1.0,
   )
   def process_batch(batch):
       # Your processing logic here
       return {"processed": batch, "status": "success"}
   ```

3. **Call the decorated function with your data:**

   ```python
   process_batch(your_data)
   ```

## Features

- **Batch Processing:** Process data in specified batch sizes.
- **Progress Tracking:** Optionally display a progress bar.
- **Retries:** Automatically retry failed batch processing with a specified delay.
- **Save Results:** Save batch results to a JSON file.
