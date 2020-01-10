--Create users

INSERT INTO "Student" (student_id,
    student_name,
    student_surname,
    student_age,
    student_spec,
    student_course,
    student_group,
    student_password) 
  VALUES (1001, 'admin', 'admin', 41, 113, 6, '----', 'adminpass');

INSERT INTO "Student" (student_id,
    student_name,
    student_surname,
    student_age,
    student_spec,
    student_course,
    student_group,
    student_password) 
  VALUES (1002, 'Василь', 'Петренко', 19, 113, 2, 'КМ-83', '11111111');

INSERT INTO "Student" (student_id,
    student_name,
    student_surname,
    student_age,
    student_spec,
    student_course,
    student_group,
    student_password) 
  VALUES (1003, 'Дмитро', 'Василенко', 18, 113, 4, 'КМ-61', '0000000');

INSERT INTO "Student" (student_id,
    student_name,
    student_surname,
    student_age,
    student_spec,
    student_course,
    student_group,
    student_password) 
  VALUES (1004, 'Петро', 'Вовк', 17, 113, 3, 'КП-71', '22222222');


INSERT INTO "Discipline" (discipline_id, discipline_name, discipline_data, tag_programming, tag_algorithm, tag_graphics, tag_databases, tag_math) 
  VALUES (1, 'Математичний аналіз', 'http://wiki.kpi.ua/math_analysis/data', false, false, false, false, true);

INSERT INTO "Discipline" (discipline_id, discipline_name, discipline_data, tag_programming, tag_algorithm, tag_graphics, tag_databases, tag_math)
  VALUES (2,  'Бази даних', 'http://wiki.kpi.ua/db/data', false, false, false, true, false);

INSERT INTO "Discipline" (discipline_id, discipline_name, discipline_data, tag_programming, tag_algorithm, tag_graphics, tag_databases, tag_math) 
  VALUES (3, 'Програмування на мові С', 'http://wiki.kpi.ua/c_programming/data', true, false, false, false, false);



INSERT INTO "Search" (search_id 
    student_id,
    search_request,
    search_request_date,
    s_tag_programming,
    s_tag_algorithm,
    s_tag_graphics,
    s_tag_databases,
    s_tag_math)
  VALUES (1, 1002, 'Математичний аналіз', 2020-01-08 18:46:48.8915, false, false, false, false, true);


INSERT INTO "Search" (search_id 
    student_id,
    search_request,
    search_request_date,
    s_tag_programming,
    s_tag_algorithm,
    s_tag_graphics,
    s_tag_databases,
    s_tag_math)
  VALUES (2, 1003, 'Бази даних', 2020-01-08 18:46:48.8915, false, false, false, true, false);


INSERT INTO "Search" (search_id 
    student_id,
    search_request,
    search_request_date,
    s_tag_programming,
    s_tag_algorithm,
    s_tag_graphics,
    s_tag_databases,
    s_tag_math)
  VALUES (3, 1004, 'Програмування', 2020-01-08 18:46:48.8915, true, false, false, false, false);


INSERT INTO "Result" (result_id 
    student_id,
    search_id,
    discipline_id,
    discipline_name,
    result_data)
  VALUES (1, 1002, 1, 1, 'Математичний аналіз', 'http://wiki.kpi.ua/math_analysis/data');



INSERT INTO "Result" (result_id 
    student_id,
    search_id,
    discipline_id,
    discipline_name,
    result_data)
  VALUES (1, 1003, 2, 2, 'Бази даних', 'http://wiki.kpi.ua/db/data');


INSERT INTO "Result" (result_id 
    student_id,
    search_id,
    discipline_id,
    discipline_name,
    result_data)
  VALUES (3, 1004, 3, 3, 'Програмування на мові С', 'http://wiki.kpi.ua/c_programming/data');


