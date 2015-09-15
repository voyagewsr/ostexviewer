
# import json
import requests
# import xml.etree.ElementTree as ET
# import lxml
from bs4 import BeautifulSoup, CData, Tag
# import markdown
# import bleach


def add_spacing(tabs=0, space='  '):
    gap = ''
    num = 0
    while num < tabs:
        gap = gap + space
        num = num + 1
    return gap


def fix_image(html):
    """"""
    locate = html.find('<img ')
    if locate >= 0:
        left = html[:locate]
        right = html[locate:]
        right = right.replace('>', ' />', 1)
        html = left + fix_image(right)
    return html

def create_tag(parent, tag_name, attrs_name=None):
    """
    Create a new tag with tag_name and its attribute attrs_name and append it as
    the child of the parent tag. 

    params:
    parent       -- the parent of the created tag
    tag_name     -- name of the tag. For example, <div> has name "div"
    attrs_name   -- optional. Name of the tag's attribute. For example, <div class="answer"> has attribute_name "answer">.

    returns:
    The created tag.
    """
    if attrs_name:
            child = Tag(name=tag_name, attrs={'class': attrs_name})
    else:
            child = Tag(name=tag_name)
    try:
            parent.append(child)
    except Exception as detail:
            print ("Get exception when appending tag:", detail)
    return child

def create_tag_with_id(parent, tag_name, attrs_name, id_number):
            #     <article class="exercise%s" id="%s-%s">
    """
    Create a new tag with tag_name and its attribute attrs_name and append it as
    the child of the parent tag. 

    params:
    parent       -- the parent of the created tag
    tag_name     -- name of the tag. For example, <div> has name "div"
    attrs_name   -- optional. Name of the tag's attribute. For example, <div class="answer"> has attribute_name "answer">.

    returns:
    The created tag.
    """

    child = Tag(name=tag_name, attrs={'class': attrs_name, 'id': id_number})
    try:
            parent.append(child)
    except Exception as detail:
            print ("Get exception when appending tag:", detail)
    return child

def add_clean_markdown(soup, tag_type, tag_class='', attribs=None):
    if(tag_class):
        # for tag in soup(tag_type, class_=tag_class):
        #    try:
                # temp = tag.string
                # tag.string = markdown.markdown(tag.string)
                # if tag.string is '' or tag.string is u'':
                #    tag.string = temp
                # tag.string = tag.string
        #    except Exception as e:
        #        print("||%s|| ||%s|| ||%s||" % (e, tag, tag.string))
        return
    if(attribs):
        marker = '$' if tag_type == 'span' else '$$'
        for tag in soup(tag_type, attrs=attribs):
            try:
                if 'CDATA' in tag['data-math']:
                    temp_tag = str(tag)
                    math = ''
                    tag_parts = temp_tag.split('"')
                    count = 0
                    if tag_parts is []:
                        break
                    # print('------------')
                    # for section in tag_parts:
                    #     print('*   ' + str(section))
                    # print('------------')
                    for section in tag_parts:
                        count += 1
                        # print('------------')
                        # print('Section Start: %s\n%s' %
                        #       (str(count), str(section)))
                        if 'CDATA' in section:
                            section = section.replace('% &lt;![CDATA[\n',
                                                      '"' + marker)
                            section = section.replace(' %]]&gt;',
                                                      marker + '"')
                            section = section.replace('% <![CDATA[\n',
                                                      marker)
                            section = section.replace(' %]]>', marker)
                            if section[:2] == '"$':
                                math = section[1:-1]
                        if str(section) == '>% </span>':
                            section = '>' + math + '</span>'
                        #     print('Equal    :', section, '\n',
                        #           str(section) == '>% </span>')
                        # else:
                        #     print('Not Equal:', section, '\n',
                        #           str(section) == '>% </span>')
                        # print('Section End  :\n' + str(section))
                        tag_parts[count - 1] = section
                        # print(tag_parts)
                    temp_tag = ''.join(tag_parts)
                    # new_tag = soup.new_tag(tag_type, )
                    # print('**************************************\n' +
                    #       temp_tag + '\n')
                tag.string.replace_with(marker + tag.string + marker)
                tag['data-math'] = '\n' if marker is '$$' else '' + \
                                   marker + tag['data-math'] + marker + \
                                   '\n' if marker is '$$' else ''
            except AttributeError:
                continue
            except Exception as e:
                raise e
        return

def add_latex(html):
    """"""
    import re
    html = re.sub("________", "", html)
    html = re.sub(r"\\rm", r"", html)  # r"\\text{", html)
    html = re.sub(r"-", r"-", html)
    html = re.sub(r"\\gt", r'&gt;', html)
    html = re.sub(r"\\lt", r'&lt;', html)
    html = re.sub(r"2!", r'2\!', html)
    html = re.sub(r",!", r",\!", html)
    html = re.sub(r"c!", r"c\!", html)
    html = re.sub(r"!\cdot!", r"\!-\cdot-\!", html)
    html = re.sub("\!$$", "$$", html)
    html = re.sub(r"2\\\\!\\!", "2", html)
    html = re.sub(r"\|", r"&#124;", html)
    html = re.sub(r"(% ((&lt;)|<)!\[CDATA\[\n)", r"", html)
    html = re.sub(r"( %]](&gt;|>))", r"", html)
    with open('index2.txt', 'w+') as output:
        output.write(html)
    soup = BeautifulSoup(html, 'html.parser')
    for nav_string in soup(text=True):
        if isinstance(nav_string, CData):
            tag = Tag(soup, name="math")
            tag.insert(0, nav_string[:])
            nav_string.replace_with(tag)
    add_clean_markdown(soup, 'span', attribs={"data-math": True})
#        for tag in soup.find_all('span', attrs={"data-math": True}):
#            tag['data-math'] = '$' + tag['data-math'] + '$'
#            try:
#                tag.string.replace_with('$' + tag.string + '$')
#            except Exception as e:
#                print(e, tag, tag.string)
    add_clean_markdown(soup, 'div', attribs={"data-math": True})
#        for tag in soup.find_all('div', attrs={"data-math": True}):
#            tag['data-math'] = '$$' + tag['data-math'] + '$$'
#            try:
#                tag.string.replace_with('$$' + tag.string + '$$')
#            except Exception as e:
#                print(e, tag, tag.string)
    add_clean_markdown(soup, 'div', tag_class='stem_text')
#        for tag in soup.find_all('div', class_='stem_text'):
#            try:
#               tag.string = bleach.clean(markdown.markdown(tag.string))
#            except Exception:
#                print("Issue: %s : %s" % (tag, tag.string))
    add_clean_markdown(soup, 'div', tag_class='answer_text')
#        for tag in soup.find_all('div', class_='answer_text'):
#            try:
#                tag.string = bleach.clean(markdown.markdown(tag.string))
#            except Exception:
#                print("Issue: %s : %s" % (tag, tag.string))
    add_clean_markdown(soup, 'div', tag_class='feedback')
#        for tag in soup.find_all('div', class_='feedback'):
#            try:
#                tag.string = bleach.clean(markdown.markdown(tag.string))
#            except Exception:
#                print("Issue: %s : %s" % (tag, tag.string))
    return soup.prettify(formatter='html')

class Portfolio(object):
    def __init__(self):
        self.problems = []
        self.total = 0

    def get_exercises(self, filename=None, url=None, number_of_questions=1):
        """"""
        if url:
            query = requests.get(url)
            try:
                data_block = query.json()
            except ValueError:
                return {}
            return data_block
        with open(filename, 'r') as f:
            return f.read()

    def import_exercises(self, location, is_url=True):
        """"""
        if is_url:
            data = self.get_exercises(url=location)
        else:
            data = self.get_exercises(filename=location)
        if 'total_count' in data:
            self.total = data['total_count']
            for exercise in data['items']:
                self.problems.append(self.to_exercise(exercise))
        else:
            self.problems.append(self.to_exercise(data))
            self.total = self.total + 1

    def to_string(self, position=0):
        """"""
        output = ""
        for key, value in self.problems[position].items():
            output = '%s%s: %s\n' % (output, key, value)
        return output

    def to_exercise(self, ex_json):
        return Exercise(ex_json)

    def to_html(self, indent=0):
        """"""
        start = None
        html = BeautifulSoup('\n', 'html.parser')
        end = None
        with open('side1.html', 'r') as left:
            start = left.read()
        with open('side2.html', 'r') as right:
            end = right.read()
        for ex in self.problems:
            html.append(ex.to_html(5))
        with open('index2.html', 'w+') as output:
            output.write(start)
            output.write(html.prettify())
            output.write(end)

    def to_csv(self, filename='ex_list.csv', tag_types=['-ex']):
        csv = 'NumAtVersion,Tag\n'
        for tag in tag_types:
            exercise_list = self.get_id_to_tags(tag)
            for exercise in exercise_list:
                csv = csv + '%s,%s\n' % (exercise, exercise_list[exercise])
        with open(filename, 'w+') as output:
            output.write(csv)

    def get_id_to_tags(self, tag_type):
        """"""
        exercise_list = {}
        for exercise in self.problems:
            for tag in exercise.tags:
                if tag_type in tag:
                    exercise_list[exercise.uid] = tag
        return exercise_list


class Exercise(object):
    def __init__(self, ex_json=None):
        self.uid = ex_json['uid'] if 'uid' in ex_json else ''
        self.number = ex_json['number'] if 'number' in ex_json else 0
        self.version = ex_json['version'] if 'version' in ex_json else 0
        self.published_at = ex_json['published_at'] \
            if 'published_at' in ex_json else ''
        self.editors = ex_json['editors'] if 'editors' in ex_json else []
        self.authors = ex_json['authors'] if 'authors' in ex_json else []
        self.copyright_holders = ex_json['copyright_holders'] \
            if 'copyright_holders' in ex_json else []
        self.derived_from = ex_json['derived_from'] \
            if 'derived_from' in ex_json else []
        self.attachments = ex_json['attachments'] \
            if 'attachments' in ex_json else []
        self.tags = ex_json['tags'] if 'tags' in ex_json else ''
        self.stimulus_html = ex_json['stimulus_html'] \
            if 'stimulus_html' in ex_json else ''
        self.question = Question(self.uid, ex_json['questions'])
        self.type = self.get_question_type(self.tags)

    def to_html(self, indent=0):
        """"""
        tags = ''
        for tag in self.tags:
            tags = tags + tag + ' '
        tags = tags[:-1]
        html = BeautifulSoup('', 'html.parser')
        article = create_tag_with_id(html, "article", "exercise " + self.type, str(self.number) + "-" + str(self.version))
        header = create_tag(article, "header")
        question_id = create_tag(header, "div", "question_id")
        h1 = create_tag(question_id, "h1")
        h1.append("ID: " + self.uid)
        published = create_tag(header, "div", "published")
        p1 = create_tag(published, "p")
        p1.append(self.published_at)
        article.append(self.question.to_html())
        footer = create_tag(article, "footer")
        question_info_wrapper = create_tag(footer, "div", "question_info_wrapper")
        question_info = create_tag(question_info_wrapper, "div", "question_info")
        h3 = create_tag(question_info, "h3")
        h3.append("Tags:")
        p2 = create_tag(question_info, "p")
        p2.append(tags)

        # html = \
        #     '''
        #     <article class="exercise%s" id="%s-%s">
        #       <header>
        #         <div class="question_id">
        #           <h1>ID: %s</h1>
        #         </div>
        #         <div class="published">
        #           <p>%s</p>
        #         </div>
        #       </header>
        #       %s
        #       <footer>
        #         <div class="question_info_wrapper">
        #           <div class="question_info">
        #             <h3>Tags:</h3>
        #             <p>%s</p>
        #           </div>
        #         </div>
        #       </footer>
        #     </article>

        #     ''' % (' ' + self.type,
        #            self.number,
        #            self.version,
        #            self.uid,
        #            self.published_at,
        #            self.question.to_html(),
        #            tags)
        return html

    def get_question_type(self, tags):
        if 'os-practice-problems' in tags or 'os-practice-concepts' in tags:
            return 'practice'
        if 'ost-chapter-review, problem' in tags or \
            'ost-chapter-review, concept' in tags or \
                'ost-chapter-review, critical-thinking' in tags:
            return 'review'
        if 'ost-test-prep, multiple-choice' in tags or \
            'ost-test-prep, short-answer' in tags or \
                'ost-test-prep, extended-response' in tags:
            return 'test_prep'
        return 'grasp_check'

    def write_to_index(self, html, target_id):
        """"""
        try:
            with open('exercises.html', 'r+') as index:
                print(index.readline())
        except Exception as e:
            print(e)

    def add_question(self, questions):
        """"""


class Question(object):
    def __init__(self, parent='', question_data=None):
        self.parent = parent
        self.answers = []
        if question_data is not None:
            self.stimulus_html = question_data[0]['stimulus_html']
            self.stem_html = question_data[0]['stem_html']
            self.hints = question_data[0]['hints']
            self.formats = question_data[0]['formats']
            self.combo_choices = question_data[0]['combo_choices']
            self.id = question_data[0]['id']
            for answer in question_data[0]['answers']:
                self.answers.append(
                    Answer(answer['id'] if 'id' in answer else 0,
                           answer['content_html'] if 'content_html' in answer
                           else '',
                           answer['correctness'] if 'correctness' in answer
                           else '0.0',
                           answer['feedback_html'] if 'feedback_html' in answer
                           else '',
                           self.parent))
            if len(self.answers) >= 1:
                self.answers.sort()
                for answer in self.answers:
                    answer.choice = '' + chr(ord('A') + answer.id -
                                             self.answers[0].id)
        else:
            self.stimulus_html = ""
            self.stem_html = ""     # **********
            self.answers = []     # **********
            self.hints = []
            self.formats = []     # **********
            self.combo_choices = []
            self.id = 0     # **********

    __eq__ = lambda self, other: self.id == other.id
    __ne__ = lambda self, other: self.id != other.id
    __lt__ = lambda self, other: self.id < other.id
    __le__ = lambda self, other: self.id <= other.id
    __gt__ = lambda self, other: self.id > other.id
    __ge__ = lambda self, other: self.id >= other.id

    def to_html(self, indent=0):
        id_number, version = self.parent.split('@')
        html = BeautifulSoup('', 'html.parser')
        question = create_tag(html, "section", "question")
        html.append(question)
        stem_question = create_tag(question, "div", "stem_question")
        stem_question.append("Question:")
        stem_text = create_tag(question, "div", "stem_text")
        stem_text.append(BeautifulSoup(add_latex(self.stem_html), 'html.parser'))
        answers = create_tag(html, "section", "answers")

        ans_num = 1
        for answer in self.answers:
            answers.append(answer.to_html())
            if ans_num < len(self.answers):
                create_tag(answers, "div", "answer_split")
                ans_num = ans_num + 1
        html.append(BeautifulSoup('</section>', 'html.parser'))     
        # html = \
        #     '''
        #     <section class="question">
        #       <div class="stem">
        #         <div class="stem_question">Question:</div>
        #         <div class="stem_text">%s</div>
        #       </div>
        #     </section>
        #     <section class="answers">
        #     ''' % add_latex(self.stem_html)
        # ans_num = 1
        # for answer in self.answers:
        #     html = html + answer.to_html()
        #     if ans_num < len(self.answers):
        #         html = html + '<div class="answer_split"></div>'
        #         ans_num = ans_num + 1
        # html = html + '</section>'
        return html


class Answer(object):
    def __init__(self, ans_id=0, content_html='', correctness='',
                 feedback_html='', parent='', letter=''):
        self.id = ans_id
        self.parent = parent
        self.correctness = correctness
        self.content_html = content_html
        self.feedback_html = feedback_html
        self.choice = letter

    __eq__ = lambda self, other: self.id == other.id
    __ne__ = lambda self, other: self.id != other.id
    __lt__ = lambda self, other: self.id < other.id
    __le__ = lambda self, other: self.id <= other.id
    __gt__ = lambda self, other: self.id > other.id
    __ge__ = lambda self, other: self.id >= other.id

    def to_html(self, indent=0):
        id_number, version = self.parent.split('@')
        html = BeautifulSoup('', 'html.parser')
        answer_wrapper = create_tag(html, "div", "answer_wrapper")
        selection = create_tag(answer_wrapper, "div", "selection")
        answer = create_tag(answer_wrapper, "div", "answer")
        correctness = create_tag(selection, "div", "correctness")
        letter = create_tag(selection, "div", "letter")
        answer_text_wrapper = create_tag(answer, "div", "answer_text_wrapper")
        feedback_wrapper = create_tag(answer, "div", "feedback_wrapper")
        check = create_tag(correctness, "span", 'check' if float(self.correctness) > 0.0 else '')
        span = create_tag(letter, "span")
        answer_text = create_tag(answer_text_wrapper, "div", "answer_text")
        feedback = create_tag(feedback_wrapper, "div", "feedback")

        span.append(self.choice + ":")
        answer_text.append(BeautifulSoup(add_latex(self.content_html), 'html.parser'))
        feedback.append(BeautifulSoup(add_latex(self.feedback_html), 'html.parser'))

        # html = \
        #     '''
        #     <div class="answer_wrapper">
        #       <div class="selection">
        #         <div class="correctness">
        #           <span class="%s"></span>
        #         </div>
        #         <div class="letter">
        #           <span>%s:</span>
        #         </div>
        #       </div>
        #       <div class="answer">
        #         <div class="answer_text_wrapper">
        #           <div class="answer_text">
        #             %s
        #           </div>
        #         </div>
        #         <div class="feedback_wrapper">
        #           <div class="feedback">
        #             %s
        #           </div>
        #         </div>
        #       </div>
        #     </div>
        #     ''' % ('check' if float(self.correctness) > 0.0 else '',
        #            self.choice,
        #            self.content_html,
        #            self.feedback_html)
        return html
