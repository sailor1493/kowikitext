# Ko-wikitext Automation

Base는 원본 리포지토리로 하되, 매 업데이트가 나올 때 마다 최신 데이터셋을 덤프하는 기능을 추가한다.

## 사용 준비

```bash
conda create -n kowiki python=3.10 -y
conda activate kowiki
pip install -r requirements.txt
```

```bash
ln -s /path/to/save/data kowiki_data
```

# Ko-wikitext

Wikitext format Korean corpus

[한국어 위키의 덤프 데이터](https://dumps.wikimedia.org/kowiki/)를 바탕을 제작한 wikitext 형식의 텍스트 파일입니다.

Corpus size
- train : 14528095 lines (868230 articles)
- dev : 76788 lines (4385 articles)
- test : 70774 lines (4386 articles)

To fetch data, run below script. Then three corpus, train / dev / test files are downloaded at ./data/

```
python fetch.py
```

This corpus is licensed with CC-BY-SA 3.0 which kowiki is licensed. For detail, visit https://www.creativecommons.org/licenses/by-sa/3.0/

## Fetch and load using Korpora

Korpora is Korean Corpora Archives, implemented based on Python. We will provide the fetch / load function at Korpora

이 코퍼스는 Korpora 프로젝트에서 사용하는 기능을 제공할 예정입니다.

```python
from Korpora import Korpora

kowikitext = Korpora.load('kowikitext')

# or
Korpora.fetch('kowikitext')
```

## License

[CC-BY-SA 3.0](https://www.creativecommons.org/licenses/by-sa/3.0/) which [kowiki](https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EC%A0%80%EC%9E%91%EA%B6%8C) dump dataset is licensed
