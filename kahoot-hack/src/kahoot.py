import html

from bs4 import BeautifulSoup

from enums import RequestMethod, RequestReturn
from wrappers._aiohttp import AiohttpSG

class KahootHack:
    
    def _get_headers(self, room_id: str):
        return {
            'accept': '*/*',
            'accept-language': 'es-419,es;q=0.9',
            'baggage': 'sentry-environment=production,sentry-release=1.3638.1,sentry-public_key=11ba66192cdb4edfbb1c297962c5809f,sentry-trace_id=153951dccf6c41c2bd364b1808637b23',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'https://kahoot.it/challenge/{room_id}',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': '153951dccf6c41c2bd364b1808637b23-b685b4eb836065c5',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
            'x-kahoot-tracking': 'platform/Web',
        }
    
    def _remove_labels(self, text: str):
        return BeautifulSoup(text, "html.parser").get_text()
    
    def _get_answers(self, response: dict):
        questions = response['kahoot']['questions']
        answers = {}
        question_index = 1
        for question in questions:
            if question['type'] in ("quiz", "open_ended"):
                questionv = self._remove_labels(question['question'])
                answer, answer_index = next(
                    (choice, idx + 1) for idx, choice in enumerate(question['choices']) if choice['correct'] == True)
                if answer.get('answer'):
                    answers = {
                        **answers,
                        question_index : { 'question': questionv, 'answer': self._remove_labels(answer['answer'])},
                    }
                else:
                    answers = {
                        **answers,
                        question_index : { 'question': questionv, 'answer': answer_index},
                    }
                question_index += 1
        return answers
    
    async def get_answers(self, room_id: str):
        response = await AiohttpSG.fetch(
            url=f'https://kahoot.it/rest/challenges/pin/{room_id}',
            request_method=RequestMethod.GET,
            request_return_type=RequestReturn.JSON,
            headers=self._get_headers(room_id),
        )
        
        return self._get_answers(response)
        