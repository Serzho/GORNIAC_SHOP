INSERT INTO product (dev_date, nicotine, vg_pg, amount_items, is_demo, is_active, product_name, description, logo_file, price, volume, rating) VALUES

('2022-03-15', 20, '60/40', 1, False, True, 'PORTWINE', 'Классический вкус всем известного портвейна. Несладкий взрослый терпкий запах способен оценить не каждый. Первая жидкость от нашей компании с незабываемым вкусом, которая никого не оставит равнодушным. Отзывы на эту жидкость всегда очень различались, но попробовать и решить для себя, достойна ли эта жидкость внимания, несомненно должен каждый!', 'static/images/logo/portwine.jpg', 350, 30, 3),
('2022-08-22', 20, '60/40', 9, False, True, 'MINESTER', 'Знаменитая жидкость, которая во время выхода произвела огромный фурор среди ценителей наших жидкостей. Вкус энергетика, кислый и при этом одновременно сладкий, прекрасно чувствующийся на вдохе и полностью раскрывающийся на выдохе. Одна из лучших жидкостей из нашей ранней линейке подарит вам незабываемые ощущения при парении, попробовав однажды, к ней хочется возвращаться снова и снова!', 'static/images/logo/minester.jpg', 350, 30, 5),
('2022-09-10', 20, '60/40', 12, False, True, 'GYM.I', 'Новейшая жидкость от нас, но при этом самая популярная и любимая среди аудитории. Сложный многогранный вкус фруктовой жвачки не даст вам остановится! Одновременно чувствуется и полная композиция, и каждый вкус отдельно, очаровывая и даря наслаждение нашему пользователю. Это та жидкость, о который ещё не было отрицательных отзывов. Советуем попробовать, возможно, вы станете первым, но мы вас уверяем, что нет <3', 'static/images/logo/gym_first.jpg', 350, 30, 3),
('2022-12-20', 20, '60/40', 0, True, True, 'GYM.II', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus odio ligula, euismod ac nulla vitae, volutpat convallis tellus. Pellentesque aliquam accumsan eros, sed elementum lacus tristique non. Etiam faucibus ex vel leo ultricies molestie. Mauris pulvinar ligula ultricies consequat luctus. Sed quis sapien risus. Nullam elit velit, convallis ut ultrices vulputate, fringilla ornare lorem.', 'static/images/logo/gym_second.jpg', 350, 30, 3),
('2022-12-20', 20, '60/40', 0, False, True, 'GYM.III', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus odio ligula, euismod ac nulla vitae, volutpat convallis tellus. Pellentesque aliquam accumsan eros, sed elementum lacus tristique non. Etiam faucibus ex vel leo ultricies molestie. Mauris pulvinar ligula ultricies consequat luctus. Sed quis sapien risus. Nullam elit velit, convallis ut ultrices vulputate, fringilla ornare lorem.', 'static/images/logo/gym_second.jpg', 350, 30, 3);

INSERT INTO item (product_id, manufacture_date, is_reserved, is_sales) VALUES
(1, '2022-09-10', False, False),
(2, '2022-09-10', False, False),
(2, '2022-09-11', False, False),
(2, '2022-08-11', False, False),
(2, '2022-09-10', False, False),
(2, '2022-09-11', False, False),
(2, '2022-08-11', False, False),
(2, '2022-09-10', False, False),
(2, '2022-09-11', False, False),
(2, '2022-08-11', False, False),
(3, '2022-09-14', False, False),
(3, '2022-09-15', False, False),
(3, '2022-09-20', False, False),
(3, '2022-09-14', False, False),
(3, '2022-09-15', False, False),
(3, '2022-09-20', False, False),
(3, '2022-09-14', False, False),
(3, '2022-09-15', False, False),
(3, '2022-09-20', False, False),
(3, '2022-09-14', False, False),
(3, '2022-09-15', False, False),
(3, '2022-09-20', False, False);

