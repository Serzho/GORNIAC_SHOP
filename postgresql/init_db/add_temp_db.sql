INSERT INTO product (dev_date, nicotine, vg_pg, amount_items, is_demo, is_active, product_name, description, logo_file, price, volume, rating) VALUES
('2022-03-15', 20, '60/40', 0, False, False, 'PORTWINE', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus odio ligula, euismod ac nulla vitae, volutpat convallis tellus. Pellentesque aliquam accumsan eros, sed elementum lacus tristique non. Etiam faucibus ex vel leo ultricies molestie. Mauris pulvinar ligula ultricies consequat luctus. Sed quis sapien risus. Nullam elit velit, convallis ut ultrices vulputate, fringilla ornare lorem.', 'static/images/logo/portwine.jpg', 350, 30, 3),
('2022-08-22', 20, '60/40', 3, False, True, 'MINESTER', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus odio ligula, euismod ac nulla vitae, volutpat convallis tellus. Pellentesque aliquam accumsan eros, sed elementum lacus tristique non. Etiam faucibus ex vel leo ultricies molestie. Mauris pulvinar ligula ultricies consequat luctus. Sed quis sapien risus. Nullam elit velit, convallis ut ultrices vulputate, fringilla ornare lorem.', 'static/images/logo/minester.jpg', 350, 30, 5),
('2022-09-10', 20, '60/40', 3, False, True, 'GYM.I', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus odio ligula, euismod ac nulla vitae, volutpat convallis tellus. Pellentesque aliquam accumsan eros, sed elementum lacus tristique non. Etiam faucibus ex vel leo ultricies molestie. Mauris pulvinar ligula ultricies consequat luctus. Sed quis sapien risus. Nullam elit velit, convallis ut ultrices vulputate, fringilla ornare lorem.', 'static/images/logo/gym_first.jpg', 350, 30, 3),
('2022-12-20', 20, '60/40', 3, True, False, 'GYM.II', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus odio ligula, euismod ac nulla vitae, volutpat convallis tellus. Pellentesque aliquam accumsan eros, sed elementum lacus tristique non. Etiam faucibus ex vel leo ultricies molestie. Mauris pulvinar ligula ultricies consequat luctus. Sed quis sapien risus. Nullam elit velit, convallis ut ultrices vulputate, fringilla ornare lorem.', 'static/images/logo/gym_second.jpg', 350, 30, 3);

INSERT INTO item (product_id, manufacture_date, is_reserved, is_sales) VALUES
(2, '2022-09-10', False, False),
(2, '2022-09-11', False, False),
(2, '2022-08-11', False, False),
(3, '2022-09-14', False, False),
(3, '2022-09-15', False, False),
(3, '2022-09-20', False, False);

