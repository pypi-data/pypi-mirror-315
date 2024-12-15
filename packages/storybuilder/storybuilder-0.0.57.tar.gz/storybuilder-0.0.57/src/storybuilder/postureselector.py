import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Now import and use Hugging Face libraries
import numpy as np
from sentence_transformers import SentenceTransformer
from .characterpostures import CHARACTER_FIGURES
from transformers import pipeline
import torch

class PostureSelector:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 检查是否有可用的 GPU
        device = 0 if torch.cuda.is_available() else -1
        self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                           model="distilbert-base-uncased-finetuned-sst-2-english", 
                                           device=device)
        
        self.posture_embeddings = self._create_posture_embeddings()

    def _generate_description(self, posture):
        parts = posture.split('-')
        return ' '.join(parts[1:])  # 移除角色类型 (boy/girl)

    def _create_posture_embeddings(self):
        posture_embeddings = {}
        for character, postures in CHARACTER_FIGURES.items():
            posture_embeddings[character] = []
            for posture in postures:
                description = self._generate_description(posture)
                embedding = self.model.encode(description)
                posture_embeddings[character].append((posture, embedding))
        return posture_embeddings

    def _analyze_sentiment(self, text):
        result = self.sentiment_analyzer(text)[0]
        return result['label'].lower()

    def get_best_posture(self, character, dialogue, position, top_k=1):
        print(f"提示：查找 {character} 的 {position} 姿势……")

        # 首先检查角色是否存在
        if character not in CHARACTER_FIGURES:
            print(f"错误：没有找到角色 {character}。")
            return None

        # 然后筛选出指定位置的姿势
        matching_postures = [p for p in CHARACTER_FIGURES[character] if f"-{position}-" in p]
        
        if not matching_postures:
            print(f"警告：没有找到 {character} 的 {position} 姿势，使用回退方案。")
            matching_postures = CHARACTER_FIGURES[character]  # 使用所有可用姿势作为回退

        if not matching_postures:
            print(f"错误：没有找到 {character} 的任何可用姿势。")
            return None

        # 对筛选后的姿势进行嵌入匹配
        sentiment = self._analyze_sentiment(dialogue)
        query = f"{sentiment} {dialogue}"
        query_embedding = self.model.encode(query)
        
        similarities = []
        for posture in matching_postures:
            embedding = next(emb for pos, emb in self.posture_embeddings[character] if pos == posture)
            similarity = np.dot(query_embedding, embedding)
            similarities.append((posture, similarity))
        
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        return [posture for posture, _ in sorted_similarities[:top_k]]

# 使用示例
if __name__ == "__main__":
    from storybuilder.characterpostures import CHARACTER_FIGURES # 修改为绝对导入

    selector = PostureSelector()
    dialogue = "哈哈，看来现在机器人比你都聪明呢！"
    best_posture = selector.get_best_posture("girl", dialogue, "stand")
    print(f"对话: {dialogue}")
    print(f"最佳姿势: {best_posture}")
