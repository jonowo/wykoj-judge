import subprocess
import threading

from fastapi import FastAPI

import constants
from judge import judge
from language import Language
from submission import Submission
from threads_manager import threads_manager

app = FastAPI()


@app.post('/judge')
def judge_solution(submission: Submission, submission_id: int, task_id: str, language: Language):
    thread_id = threads_manager.get_new_thread_id()
    while thread_id >= constants.MAX_THREAD_NO:
        thread_id = threads_manager.get_new_thread_id()
    thread = threading.Thread(target=judge, args=[submission.source_code, submission_id, task_id, language, thread_id],
                              daemon=True)
    thread.start()
    return {}


@app.get('/')
def home():
    return '''必要的沉默
今天發生了一件事情，當時我想要力陳己見，最後選擇了沉默。我認為沉默是必要的。
「允行，先不要坐在沙發上，等我整理好神枱，過來拜拜，才坐回沙發上。」外婆彎着身子，語重心長地對我説。
我不耐煩地站起了身，並坐在飯桌旁的椅子上。想起上周新聞提到一個有關燒香的研究指出在室內燒香會釋出致癌物，令癌症如肺癌更容易發生。我看着外婆那蒼白的頭髮；憔悴的面容；彎曲的身子，就想到外婆已經年邁，也不希望外婆的健康出現任何的問題。
從小時候起，每一次來到外婆家中，都看到沙發旁淺啡色的櫃子，櫃子的正中設有一塊紅底金子的牌，兩旁則放有兩片孔雀花紋的羽毛和束着兩條鮮紅色的絲帶。左右兩則放着各一個香爐，正上方則有一塊半圓狀的反光金屬，中間放着新鮮的水果。
「允行，幫我從桌子上的紅色膠袋中拿柚子過來。」外婆一邊仔細地布抹去神主牌上的塵，一邊説。我聽到後便從膠袋中拿出柚子，左手拿着手提電話，右手則提着柚子，並邊看手機，邊走到外婆身旁遞過柚子。
「舉頭三尺有神明，一定要有敬畏之心。允行，下次再要拿用來拜神的水果，一定要用雙手捧着才是對神明的尊敬。」外婆邊接過柚子，邊慈祥地説道。外婆把柚子放在紅色的盤子上，便繼續用布慢慢地櫃子裏的塵。神主牌上那反光的金屬映出外婆的眼神，既帶着一絲不苟的目光，又不失對神明的敬仰。
我看着外婆整理神枱的身影，便明白到外婆燒香拜神是為了對神明的敬畏。但是我始終認為外婆身體的健康比甚麼都重要，正當我想叫外婆不要再燒香拜神時，外婆拿出了線香，並熟練地用打火機點燃，然後用手扇熄線香的火焰，外婆家中頓時彌漫着一陣白煙。
外婆跪在神枱前，合着雙手搖晃，並喃喃地説：「希望允行一家能夠平平安安、健健康康……」此時我明白到外婆拜神除了是對神明敬畏，也是為了家人的平安，我便暫時選擇了沉默，不再阻止外婆拜神。
「允行，過來請請吧。」外婆對我説。
我走到神台前跪下，閉上了眼睛，並合着雙手搖晃，心中想着：希望外婆能健健康康……
我張開了雙眼，凝視着香爐內的香，香的頂部燃燒時發出通透的橙黃色，頂端有燒至彎曲的煙灰。煙灰越燒越長，燒斷了便掉在香爐中，一陣白煙隨之飄出，暫留在半空中，隨風而散。
等香燒完後，我和外婆吃過晚飯，便離開了外婆家。我在路邊截了的士回家，在回家的路途上，我一直反省着到底我剛才的決定是對或錯。
其實對事情的沉默，並不是逃避，更不是麻木的表現，而沉默往往卻是最理智、冷靜的表現。如果我當面勸外婆不要再燒香拜神，避免身體出任何問題，外婆很大機會因為自己的信仰而不會接納我的意見，更有可能會與我吵架，以不和收場。我固然不希望事情會發展成這樣的地步，因此我認為沉默是必要的。選擇了沉默的時候，能帶給我更多的思考時間，更能避免冒犯外婆。而更多的思考時間，亦能讓我作出更好的決定。
我回到家中，便打電話給外婆。
「喂，婆婆，我是允行，下星期六你有空嗎？不如我陪你到醫院做一次身體檢查吧。」'''


@app.on_event('startup')
def startup():
    # cleanup sandbox
    cleanup_proc = subprocess.run(['isolate', '--silent', '--cleanup'])
    assert cleanup_proc.returncode == 0
