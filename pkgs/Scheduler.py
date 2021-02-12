from datetime import datetime, timedelta

eng_suffix = ['s', 'm', 'h', 'd', 'w']
kor_suffix = ['초', '분', '시간', '일', '주']
suffix_value = [1, 60, 3600, 3600 * 24, 3600 * 24 * 7]

class Duration:
    def __init__(self, text):
        if type(text) == str: self.value = timedelta(seconds = self.text2secs(text))
        else: self.value = text

    def text2secs(self, text):
        prefix = ''
        suffix = text
        for c in text:
            if not c.isdigit(): break
            prefix += c
        suffix = suffix[len(prefix):]
        for suffix_list in eng_suffix, kor_suffix:
            if suffix in suffix_list:
                return suffix_value[suffix_list.index(suffix)] * int(prefix)
        raise ValueError

    def to_secs(self): return self.value.total_seconds()
    def to_kortext(self): return self._to_text('kor')
    def to_engtext(self): return self._to_text('eng')
    def _to_text(self, mode):
        suffix_list = eng_suffix if mode == 'eng' else kor_suffix
        seconds = self.to_secs()
        for i in range(4 if seconds > 0 else 0, -1, -1):
            if seconds % suffix_value[i] == 0:
                return str(int(seconds // suffix_value[i])) + suffix_list[i]

class Schedule:
    def __init__(self, duration):
        self.value = datetime.now() + Duration(duration).value
    def __str__(self): return str(self.value)
    def is_done(self): return datetime.now() > self.value
    def time_left(self): return Duration(datetime.now() - self.value)

if __name__ == '__main__':
    s = Schedule(input('dur:'))
    while True:
        if s.is_done(): break
    print('done!')
