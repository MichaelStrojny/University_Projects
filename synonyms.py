import math

def norm(vec):
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += x * x  
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    sum = 0.0
    for word in vec1:
        if word in vec2:
            sum += vec1[word] * vec2[word]
    if norm(vec1.values()) == 0.0 or norm(vec2.values()) == 0.0:
        return -1
    return sum / (norm(vec1.values()) * norm(vec2.values()))

def build_semantic_descriptors(sentences):
    big_dict = {}
    for sentence in sentences:  
        L = set(sentence)
        for word in L:  
            if word not in big_dict:
                    big_dict[word] = {}
            for wordd in L:  
                if wordd != word:
                    if wordd not in big_dict[word]:
                        big_dict[word][wordd] = 1
                    else:
                        big_dict[word][wordd] += 1
    return big_dict

def build_semantic_descriptors_from_files(filenames):
    deep_storage = []
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            text = f.read().lower()
            text = text.replace(":", '').replace(";", '').replace(",", '').replace("-", ' ').replace("--", ' ').replace('"', '').replace("!", ".").replace("?", ".").replace("\n", ".")
            sentences = text.split(".")
            for sentence in sentences:
                words = sentence.split()
                if words:
                    deep_storage.append(words)
    return build_semantic_descriptors(deep_storage)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]
    max_s = -1
    winner = choices[0]
    for choice in choices:
        if choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
            if similarity > max_s:
                max_s = similarity
                winner = choice
    return winner

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    true = 0.0
    total = 0.0
    with open(filename, "r", encoding="latin1") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if most_similar_word(parts[0], parts[2:], semantic_descriptors, similarity_fn) == parts[1]:
                true += 1
            total += 1
    return (true / total) * 100

