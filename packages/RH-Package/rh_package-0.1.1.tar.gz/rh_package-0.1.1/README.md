# Evaluation of Relation Hallucination in Abstractive Summarization:

## Features

## 1. Relation Extraction for Varied Models

### Comprehensive SVO Relation Extraction

- Extracts **Subject-Verb-Object (SVO)** relations from:
  - **Input Text (InputText)**
  - **Reference Summaries (ReferenceSummary)**
  - **Model-Generated Summaries** for varied models.
- Includes **confidence levels** for each extracted relation to ensure reliability.

---

## 2. Computing Hallucination Factors

### Advanced Hallucination Metrics

- Evaluates hallucination tendencies in model-generated summaries based on:
  - Relation overlaps between **InputText**, **ReferenceSummary**, and **model summaries**.
- Computes custom hallucination metrics dynamically for each model:
  - **Precision**
  - **Recall**
  - **F1 Score**
  - **6 Hallucination metrics namely Extractiveness factor , Negative and Postive Hallucinations , Lost Hallucinations and Lost Focus, Overfocus factor**

### Relation Matching

- Converts extracted SVO relations into structured tuples to facilitate direct comparison.
- Measures hallucination factors based on relation alignment or mismatch.

---

## 3. Additional Highlights

### Multi-Model Compatibility

- Easily integrates summaries from multiple models in a single dataset.
- Provides **comparative metrics** for each model’s output.

### Customizable Field Mapping

- Allows flexible mapping of fields for datasets with varying structures.
- Ensures compatibility with diverse data formats.

### Efficient Processing

- Handles both single-entry and batch processing.
- Scalable for datasets of any size, from small samples to large datasets.

---

## Usage

This framework and package is designed for researchers and developers working on abstractive summarization and hallucination analysis, offering robust tools for multi-model evaluation and relation extraction in text summarization models.

## Installation

Please install our package using following command:

```bash
pip install RH_Package
```

# Functionality 1:

# Processing the single data and batch data for Relation Hallucination in text summarization models using our pacakage:

## package name: process_text_and_compute_metrics

### How to import?

from RHI_Metrics import process_text_and_compute_metrics

### What feature and functionality this provides?

- **Extract SVO Relations**: Extracts Subject-Verb-Object relations with confidence scores from input text, reference summary, and model-generated summaries.
- **Compute ROUGE Scores**: Computes ROUGE-1, ROUGE-2, and ROUGE-L scores for model-generated summaries against the reference summary.
- **Compute Hallucination Metrics**: Computes metrics related to hallucinations, including precision, recall, F1 score, 6 factors namely Extractiveness factor , Negative and Postive Hallucinations , Lost Hallucinations and Lost Focus, Overfocus factor respectively and more, by comparing generated and reference SVO relations.
- **Supports Single and Batch Processing**: Can process individual entries or a list of entries in batch mode.
- **Customizable Field Mapping**: Allows customization of field names for input text and reference summary.

### Installation

These are the packages need to be installed:

```bash
pip install nltk rouge-score rouge-score numpy pandas scipy transformers matplotlib seaborn streamlit

python -m spacy download en_core_web_sm


```

### How to Use?

### ** Function: process_text_and_compute_metrics **

This function processes JSON data to extract relations, compute ROUGE scores, and hallucination metrics. It works for both single-entry and batch processing.

#### Function Strcture:

#### How to import??

```python
from RH_Package.RH_Metrics.RH_Metrics import process_text_and_compute_metrics
```

#### def process_text_and_compute_metrics(

#### data: Union[Dict, List[Dict]],

#### batch_mode=True,

#### field_mapping: Dict = None

#### ) -> List[Dict]:

#### Arguments:

- **`data`** (`Union[Dict, List[Dict]]`):
  - For batch processing (`batch_mode=True`), provide a list of dictionaries where each dictionary represents an entry.
  - For single-entry processing (`batch_mode=False`), provide a single dictionary.
- **`batch_mode`** (`bool`, default=True):
  - If `True`, processes multiple entries.
  - If `False`, processes a single entry.
- **`field_mapping`** (`Dict`, optional):
  - A dictionary to map custom field names for input text and reference summary.  
    Example: `{"input_text": "textInput", "reference_summary": "summaryReference"}`.

#### Returns:

- `List[Dict]`: A list of processed entries containing extracted relations, ROUGE scores, and hallucination metrics for each model.

---

### Example

#### Single Entry Processing:

```python
from RH_Package.RH_Metrics.RH_Metrics  import process_text_and_compute_metrics

data = {
    "textInput": "This is an input text.",
    "summaryReference": "This is a reference summary.",
    "facebook/bart-large-cnn": "Generated summary by BART.",
    "google/pegasus-xsum": "Generated summary by Pegasus."
}

field_mapping = {
    "input_text": "textInput",
    "reference_summary": "summaryReference"
}

result = process_text_and_compute_metrics(data, batch_mode=False, field_mapping=field_mapping)
print(result)
```

### For Batch Processing here is an example below:

```python
json_data = [
    {
        "textInput": "This is input text for the first entry.",
        "summaryReference": "This is the reference summary for the first entry.",
        "facebook/bart-large-cnn": "Generated summary by BART.",
    },
    {
        "content": "This is input text for the second entry.",
        "ref_summary": "This is the reference summary for the second entry.",
        "google/pegasus-xsum": "Generated summary by Pegasus.",
    }
]

field_mapping = {
    "input_text": "textInput",
    "reference_summary": "summaryReference"
}

result = process_text_and_compute_metrics(json_data, batch_mode=True, field_mapping=field_mapping)
print(result)
```

#### Customizing Field Names

#### If your JSON data or your data uses different field names for input text and reference summary, you can provide a custom field mapping dictionary.

```python

field_mapping = {
    "input_text": "customInputTextField",
    "reference_summary": "customReferenceSummaryField"
}
```

### Sample Data Format

```json
{
  "0": {
    "Id": "10157432",
    "dataset": "xlsum",
    "InputText": "The announcement makes Italy the latest eurozone country to announce cuts in an effort to reduce the gap between spending and earnings. The UK and Danish governments also this week announced plans to curb spending. Italy will take measures to reduce public sector pay and will put a freeze on new recruitment. Public sector pensions and local government spending are also expected to be hit. Added to these, a clampdown on tax avoidance is also planned. The cuts are equal to some 1.6% of gross domestic product (GDP). Similar reductions in spending measures have already been announced by Greece, Spain and Portugal. Heavy price Some Italian workers have already been out protesting. In Rome, workers at the Italian Institute for the Professional Development of Vocational Training of Workers (Isfol) held protests against the cuts at their headquarters. One worker, Simone Casadei, said the public sector had already paid a heavy price. The sector of public research has already paid its toll and suffered cuts in the past, he said. So we are asking for our sector to be left out of the new budget cuts. He added that the money should be raised by getting tough on tax evasion. We also demand that the money needed to face this problems... is obtained through a tough action against tax evasion. The state cannot always take the money from the same sources, that is workers and pensioners. The government hopes to bring its deficit down to below 3% of GDP by 2012 - from 5.3% now - in order to help maintain the confidence of international investors and prevent the spread of a Greek-style debt crisis. Concerns over the level of Greece's debts have led to an effective boycott of Greek debt on the world markets, and have spilled over into deepening worries about the other weakest members of the 16-nation eurozone: Spain, Portugal and Italy.",
    "ReferenceSummary": "The Italian government has approved austerity measures worth 24 billion euros (\u00a320bn; $29bn) for the years 2011-2012.",
    "facebook/bart-large-cnn": "Italy will take measures to reduce public sector pay and will put a freeze on new recruitment. Public sector pensions and local government spending are also expected to be hit. The cuts are equal to some 1.6% of gross domestic product (GDP) Similar reductions in spending measures have already been announced by Greece, Spain and Portugal.",
    "google/pegasus-xsum": "The Italian government has announced plans to cut public sector spending by 20bn (\u00a314bn; $22bn) over the next two years.",
    "t5-large": "the cuts are equal to some 1.6% of gross domestic product (gdp) similar reductions in spending measures have already been announced by Greece, Spain and Portugal. the government hopes to bring its deficit down to below 3% of GDP by 2012.",
    "gpt-3.5-turbo": "Italy has announced public sector spending cuts of 1.6% of GDP in an attempt to reduce the gap between spending and earnings and to bring its deficit down to below 3% of GDP by 2012. Measures will include a reduction in public sector pay, a freeze on new recruitment, a clampdown on tax avoidance as well as cuts to public sector pensions and local government spending. Italy becomes the latest eurozone country to announce such cuts after similar moves made by Greece, Spain and Portugal. Although the government hopes to prevent the spread of a Greek-style debt crisis, the proposed austerity measures have already drawn protests from some public sector workers.",
    "RefSum": "The Italian government has approved austerity measures worth 24 billion euros (\u00a320bn; $29bn) for the years 2011-2012."
  }
}
```

#### Explanation of Fields:

- Id: Unique identifier for the data sample.
- dataset: The dataset source (e.g., xlsum).
- InputText: The input article or passage used as the base for summarization.
- ReferenceSummary: The gold-standard reference summary.
- facebook/bart-large-cnn, google/pegasus-xsum, t5-large, gpt-3.5-turbo:
  Summaries generated by different models.
- RefSum: Alternative representation of the reference summary (same as ReferenceSummary in this example).

## Computation of Hallucination metrics Separately Using _ calculate_hallucination_factors_:

Package name: calculate_hallucination_factors

Function Parameters:

pred_words: Tokenized predicted (generated) words.
ref_words: Tokenized reference summary words.
inp_words: Tokenized input text words.

input_relations: SVO relations extracted from the input text.
ref_relations: SVO relations extracted from the reference summary.
model_relations: SVO relations extracted from the predicted summary.

Function Output:
Returns a dictionary containing:

Metrics:

precision: Precision of the generated relations.
recall: Recall of the generated relations.
f1_score: F1 score for the generated relations.
ef (Extractiveness Factor): Measures overlap between input, reference, and generated relations.
ph (Positive Hallucination): Evaluates agreement between reference and generated relations.
of (Over Focus): Quantifies excessive focus on input relations.
nh (Negative Hallucination): Reflects spurious content in generated relations.
lf (Lost Focus): Indicates missing content from reference relations.
lh (Lost Hallucination): Highlights divergence between input and generated relations.
rhi (Relation Hallucination Index): A composite metric summarizing hallucination behavior.
Intersection Counts:

I_intersect_R_count: Overlap between input and reference relatzions.
I_intersect_G_count: Overlap between input and generated relations.
R_intersect_G_count: Overlap between reference and generated relations.
I_intersect_R_intersect_G_count: Triple overlap between input, reference, and generated relations.

Set Lengths:

lenI: Length of input relations set.
lenR: Length of reference relations set.
lenG: Length of generated relations set.

```python
from RH_Package.RH_Metrics.RH_Metrics  import calculate_hallucination_factors
pred_words=["The", "Eiffel", "Tower", "is", "a", "landmark"],
ref_words=["Eiffel", "Tower", "is", "a", "famous", "landmark"],
inp_words=["The", "Eiffel", "Tower", "is", "a", "famous", "site"],
input_relations=[("Eiffel Tower", "is", "landmark")],
ref_relations=[("Eiffel Tower", "is", "famous landmark")],
model_relations=[("Eiffel Tower", "is", "landmark")]

metrics = calculate_hallucination_factors(pred_words, ref_words, inp_words, input_relations, ref_relations, model_relations)

print(metrics)
```

## Extracting Relations for Any Given Text

This package includes a powerful algorithm to extract Subject-Verb-Object (SVO) relations from any text with confidence scores. You can use the following function to extract these relations:

### Function Name:

#### extract_relations_and_svo_with_confidence_score(input_text)

#### HOw to import??

```python
from RH_Package.RH_Metrics.RH_Metrics import xtract_relations_and_svo_with_confidence_score
```

### Parameters:

- **`text`**: The input text for which you want to extract SVO relations.
- **`confidence_threshold`**: (Optional, default = 0.5) The minimum confidence score required for a relation to be included in the output.

### Usage:

Pass your input text and the desired confidence threshold to the function to extract relations.

### Example:

````python
from RH_Package.RH_Metrics.RH_Metrics import extract_relations_and_svo_with_confidence_score

# Input text
text = "The Italian government has approved austerity measures worth 24 billion euros for the years 2011-2012."

# Extract relations with a confidence threshold of 0.6
relations = extract_relations_and_svo_with_confidence_score(text, confidence_threshold=0.6)

# Sample Output
print(relations)

```
[
{"subject": "Italian government", "verb": "approved", "object": "austerity measures", "confidence": 0.8},
{"subject": "austerity measures", "verb": "worth", "object": "24 billion euros", "confidence": 0.75}
]
````

## Function for Rouge score:

```python
from RH_Package.RH_Metrics import compute_all_rouge_scores
```

#### If you want calculate only rouge score for your data then use function compute_all_rouge_scores(predicted, reference)

## pass the function with generated summary and reference text

## Conclusion

This package serves as a comprehensive tool for evaluating relation hallucination in abstractive summarization models. By focusing on Subject-Verb-Object (SVO) relations, it provides detailed metrics to measure and compare model behavior, helping researchers identify and mitigate hallucination issues in generated summaries.

The flexibility of batch processing, customizable field mappings, and compatibility with multiple models makes it suitable for handling diverse datasets and research requirements. With features like precision metrics, hallucination factors, and multi-model analysis, this package offers valuable insights for improving the reliability and quality of abstractive text summarization systems.

Contributions, suggestions, and enhancements are always welcome. Together, we can refine and expand the capabilities of this package for the benefit of the research community.
