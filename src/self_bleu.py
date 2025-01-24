import ast
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import pandas as pd
def calculate_self_bleu_with_smoothing(generated_sequences, n_gram=4):
    """
    Calculate Self-BLEU for a set of generated sequences with smoothing.

    Args:
        generated_sequences (list of str): List of generated sequences.
        n_gram (int): Maximum n-gram order for BLEU (default: 4).
    
    Returns:
        float: Average Self-BLEU score with smoothing.
    """
    total_bleu = 0.0
    count = len(generated_sequences)

    # Define weights for n-grams (BLEU-1 to BLEU-n_gram)
    weights = tuple(1.0 / n_gram for _ in range(n_gram))
    
    # Use smoothing function from nltk
    smooth_fn = SmoothingFunction().method1
    
    for i, candidate in enumerate(generated_sequences):
        references = [seq.split() for j, seq in enumerate(generated_sequences) if j != i]
        candidate_tokens = candidate.split()
        
        # Calculate BLEU score for the current candidate with smoothing
        bleu = sentence_bleu(references, candidate_tokens, weights, smoothing_function=smooth_fn)
        total_bleu += bleu

    # Average Self-BLEU score
    return total_bleu / count

# Example usage
generated_sequences = [
    "the cat sits on the mat",
    "a dog runs in the park",
    "birds fly in the sky",
    "the cat sits on the mat"
]

self_bleu_score = calculate_self_bleu_with_smoothing(generated_sequences)
print(f"Self-BLEU with Smoothing: {self_bleu_score}")
def get_text_question(d):

    context = d["context"]
    question = d["question"]
    correct_answer = d["correct_answer"]
    distractor_options = d["distractor_options"]
    ret = f"Question: {context} {question} Options: {correct_answer} {distractor_options}"
    return ret
if __name__ == "__main__":
    df1 = pd.read_csv('data/gpt4_eval_data/gpt_4_pref_machine_data_complete.csv')
    # df2 = pd.read_csv('data/gpt4_eval_data/gpt_4_pref_machine_data_complete.csv')
    data_dict = df1.to_dict('records')
    init_qs = [get_text_question(ast.literal_eval(d['init_question'])) for d in data_dict]
    pl_qs = [get_text_question(ast.literal_eval(d['best_pl_question'])) for d in data_dict]
    # breakpoint()
    self_bleu_init = calculate_self_bleu_with_smoothing(init_qs)
    self_bleu_pl = calculate_self_bleu_with_smoothing(pl_qs)
    print("Init questions self-bleu: ",self_bleu_init)
    print("PL questions self-bleu: ",self_bleu_pl)