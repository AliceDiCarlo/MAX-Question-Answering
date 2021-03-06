#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest
import requests
import json


def test_multiple_paragraphs():
    model_endpoint = 'http://localhost:5000/model/predict'
    json_data = [{
                    "id": 1,
		            "title": "Computer Science Department University of Crete",
		            "text": "The Computer Science Department of the University of Crete operates since 1984, historically the second Computer Science Department to operate in Greece. The Computer Science Department belongs to the School of Sciences and Engineering, which operates in Heraklion. The School was founded as School of Physical & Mathematical Sciences in 1973 and renamed as the School of Science in 1984. The Department of Computer Sciences was established in 1983. In FEK 388 / 5.7.83 was conversion and distribution of vacancies at the University of Crete and was first given to the Department of Computer Science 13 faculty positions.  The graduate program of the Department began operating in 1985 as \"Master Program in Computer Science\". In 1992 all postgraduate studies in Greece were organized under N2083 / 1992 (FEK159 / A / 21.09.1992) Chapter V \"Graduate Studies\" which replaced Article 81 of Law 1566/1985 and was based on Postgraduate Studies Regulation of the Department, on the proposal of the Department to the Ministry of Education for the modernization of postgraduate studies in Greece. From February 1994 works with the Senate and after approval of the program by the Ministry of Education (FEK 866 / 11.26.93). In 2003 (FEK1694 / vol.B '/ 11.19.2003) renewed operation of the Postgraduate Studies Program and the academic year 2014-2015 operates on the revised Postgraduate Studies Program (PSP) entitled \"Science and Computer Engineering\".  The Department gradually staffed by excellent scientists. The Computer Science Department elected the first faculty in 1981 and became operational in 1984 so accepted and the first undergraduates. In February 1985 the postgraduate program was established. Today the department has twenty-one (21) Professors and regularly hosts academic scholars as visiting faculty professors.  At thirty-five (35) years of operation has developed and implemented a modern curriculum. Today, a significant contribution to higher education in our country in science and computer technology issues are recognized by educational work at the undergraduate and graduate level, with quality acclaimed internationally.  The Department even since its establishment, had a strong research orientation. Since the inception of the Department works closely with the Institute of Computer Science (ICS) of the Foundation for Research and Technology Hellas (FORTH). This cooperation, which continues today, creates an excellent environment for research and education. The research of the Department now enjoys international recognition. Members of the Department throughout the history of the Department and even more today, hold important international collaborations with leading academic and research institutions and also with industry in areas of crucial interest.  The Department is recognized today as one of the top departments in computer science in the country.  Based on a recent study of the work of the Departments of Computer Engineering and Computer Science of  the country based on bibliographical indices, the Department of Computer Science was ranked first among all departments.",
	            	"qa": [{
				        "question": "When was the postgraduate program established?",
				        "answer": "February 1985/1985",
				        "entity": "DATE",
				        "note": "group A, factoid, verbatim"
			    }]
        
    r = requests.post(url=model_endpoint, json=json_data)
    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'


def test_response():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'samples/small-dev.json'

    with open(file_path, 'rb') as file:
        json_data = json.load(file)
        r = requests.post(url=model_endpoint, json=json_data)

    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'

    with open(file_path) as file:
        q_objs = json.load(file)["qa"]["question"]

        # make sure all the correct questions have been returned
        all_questions = [q for q in q_objs]
        all_responses = response["predictions"][0]

        assert len(all_questions) == len(all_responses)

        # make sure answers are nonempty
        # note that this is not expected. However, for the questions in samples/small-dev, it is reasonable to
        # expect this model to at least provide an answer
        assert "" not in all_responses


if __name__ == '__main__':
    pytest.main([__file__])
