:- use_module(library(csv)).
:- use_module(library(http/json)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).

% Load student data from CSV
load_data(File) :-
    csv_read_file(File, Rows, [functor(student), arity(4)]),
    maplist(assert, Rows).

% Scholarship eligibility rule
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, _, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

% Exam permission rule
permitted_for_exam(Student_ID) :-
    student(Student_ID, _, Attendance, _),
    Attendance >= 75.

% REST API Endpoints
:- http_handler(root(eligibility), handle_eligibility, []).
:- http_handler(root(debarred), handle_exam_permission, []).

% Start the server
start_server(Port) :-
    http_server(http_dispatch, [port(Port)]).

% Check scholarship eligibility
handle_eligibility(Request) :-
    http_read_json_dict(Request, Dict),
    Student_ID = Dict.student_id,
    (   eligible_for_scholarship(Student_ID)
    ->  Response = _{student_id: Student_ID, scholarship: "Eligible"}
    ;   Response = _{student_id: Student_ID, scholarship: "Not Eligible"}
    ),
    reply_json_dict(Response).

% Check exam permission
handle_exam_permission(Request) :-
    http_read_json_dict(Request, Dict),
    Student_ID = Dict.student_id,
    (   permitted_for_exam(Student_ID)
    ->  Response = _{student_id: Student_ID, exam_permission: "Allowed"}
    ;   Response = _{student_id: Student_ID, exam_permission: "Debarred"}
    ),
    reply_json_dict(Response).

