-- Создание последовательности
CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- Использование последовательности в таблице
CREATE TABLE users (
    id INTEGE DEFAULT nextval('user_id_seq') PRIMARY KEY,
    name VARCHA(100) NOT NULL,
    email VARCHA(100) UNIQUE NOT NULL
);

-- Вставка с использованием последовательности
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Получение текущего значения последовательности
SELECT currval('user_id_seq');

-- Изменение последовательности
ALTER SEQUENCE user_id_seq RESTART WITH 1000;

-- Удаление последовательности
DROP SEQUENCE IF EXISTS user_id_seq;

-- Простое представление
CREATE VIEW active_users AS
SELECT id, name, email
FROM users
WHERE is_active = TRUE;

-- Обновляемое представление
CREATE VIEW user_profiles AS
SELECT u.id, u.name, u.email, p.bio, p.avatar_url
FROM users u
LEFT JOIN profiles p ON u.id = p.user_id;

-- Использование представления
SELECT * FROM active_users WHERE name LIKE 'J%';

-- Материализованное представление
CREATE MATERIALIZED VIEW expensive_products AS
SELECT id, name, price
FROM products
WHERE price > 1000
WITH DATA;

-- Обновление материализованного представления
REFRESH MATERIALIZED VIEW expensive_products;

-- Изменение представления
ALTER VIEW active_users RENAME TO enabled_users;

-- Удаление представления
DROP VIEW IF EXISTS user_profiles;

-- Простой CTE
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
)
SELECT region, total_sales
FROM regional_sales
WHERE total_sales > 1000000;

-- Рекурсивный CTE
WITH RECURSIVE employee_hierarchy AS (
    -- Базовый случай
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Рекурсивный случай
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT id, name, level
FROM employee_hierarchy
ORDER BY level, name;

-- Несколько CTE в одном запросе
WITH 
departments_stats AS (
    SELECT department_id, COUNT(*) AS emp_count, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
),
high_paid_depts AS (
    SELECT department_id
    FROM departments_stats
    WHERE avg_salary > 50000
)
SELECT d.name, ds.emp_count, ds.avg_salary
FROM departments d
JOIN departments_stats ds ON d.id = ds.department_id
WHERE d.id IN (SELECT department_id FROM high_paid_depts);


-- Скалярный подзапрос
SELECT name, 
       (SELECT COUNT(*) FROM orders WHERE user_id = users.id) AS order_count
FROM users;

-- Подзапрос в FROM
SELECT u.name, o.order_total
FROM users u
JOIN (
    SELECT user_id, SUM(amount) AS order_total
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;

-- Подзапрос в WHERE
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- Подзапрос с EXISTS
SELECT id, name
FROM customers
WHERE EXISTS (
    SELECT 1 FROM orders 
    WHERE orders.customer_id = customers.id AND orders.amount > 1000
);

-- Подзапрос с IN
SELECT name
FROM products
WHERE category_id IN (
    SELECT id FROM categories WHERE name LIKE 'Electronics%'
);

-- Коррелированный подзапрос
SELECT e1.name, e1.salary
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
);

-- Подзапрос в HAVING
SELECT department_id, AVG(salary) as avg_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) > (
    SELECT AVG(salary) FROM employees
);

-- Представление с подзапросами и CTE
CREATE VIEW customer_order_stats AS
WITH order_summary AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_orders,
        SUM(amount) AS total_spent,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
),
high_value_customers AS (
    SELECT customer_id
    FROM order_summary
    WHERE total_spent > 10000
)
SELECT 
    c.id,
    c.name,
    c.email,
    os.total_orders,
    os.total_spent,
    os.last_order_date,
    CASE WHEN hvc.customer_id IS NOT NULL THEN 'High Value' ELSE 'Regular' END AS customer_type
FROM customers c
LEFT JOIN order_summary os ON c.id = os.customer_id
LEFT JOIN high_value_customers hvc ON c.id = hvc.customer_id;

-- Последовательность + представление + подзапрос
CREATE SEQUENCE report_id_seq;

CREATE TABLE monthly_reports (
    id INTEGE DEFAULT nextval('report_id_seq') PRIMARY KEY,
    report_month DAT,
    generated_by INTEGE,
    content TEX
);

CREATE VIEW recent_reports AS
SELECT r.id, 
       to_char(r.report_month, 'YYYY-MM') AS month,
       u.name AS generated_by_name,
       r.content
FROM monthly_reports r
JOIN users u ON r.generated_by = u.id
WHERE r.report_month >= (SELECT MAX(report_month) - INTERVA '6 months' 
                         FROM monthly_reports);

-- Сложный запрос с CTE, подзапросами и агрегацией
WITH 
product_sales AS (
    SELECT 
        p.id AS product_id,
        p.name AS product_name,
        c.name AS category_name,
        SUM(oi.quantity) AS total_quantity,
        SUM(oi.quantity * oi.unit_price) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.id = oi.product_id
    JOIN categories c ON p.category_id = c.id
    GROUP BY p.id, p.name, c.name
),
category_stats AS (
    SELECT 
        category_name,
        COUNT(DISTINCT product_id) AS product_count,
        SUM(total_quantity) AS category_quantity,
        SUM(total_revenue) AS category_revenue
    FROM product_sales
    GROUP BY category_name
)
SELECT 
    ps.product_name,
    ps.category_name,
    ps.total_quantity,
    ps.total_revenue,
    ps.total_revenue / NULLIF(ps.total_quantity, 0) AS avg_price_per_unit,
    (ps.total_revenue / NULLIF(cs.category_revenue, 0)) * 100 AS revenue_percentage
FROM product_sales ps
JOIN category_stats cs ON ps.category_name = cs.category_name
WHERE cs.category_revenue > 10000
ORDER BY ps.category_name, ps.total_revenue DESC;



SELECT 
	Н_ОЦЕНКИ.КОД, 
	Н_ВЕДОМОСТИ.ДАТА 
FROM Н_ВЕДОМОСТИ 
	INNER JOIN Н_ОЦЕНКИ 
		ON Н_ВЕДОМОСТИ.ОЦЕНКА = Н_ОЦЕНКИ.КОД 
WHERE 
	Н_ОЦЕНКИ.КОД > '2' 
	AND Н_ВЕДОМОСТИ.ИД = '1250972';

SELECT Н_ЛЮДИ.ИД,
       Н_ОБУЧЕНИЯ.НЗК,
       Н_УЧЕНИКИ.НАЧАЛО
FROM Н_ОБУЧЕНИЯ
    INNER JOIN Н_ЛЮДИ
        ON Н_ЛЮДИ.ИД = Н_ОБУЧЕНИЯ.ЧЛВК_ИД
    INNER JOIN Н_УЧЕНИКИ
        ON Н_УЧЕНИКИ.ИД = Н_ОБУЧЕНИЯ.ЧЛВК_ИД
WHERE Н_ЛЮДИ.ИМЯ > 'Владимир'
      AND Н_ОБУЧЕНИЯ.НЗК > '001000'
      AND Н_УЧЕНИКИ.ГРУППА < '3100';

SELECT COUNT(*)
FROM (
	SELECT ОТЧЕСТВО
	FROM Н_ЛЮДИ
	GROUP BY ОТЧЕСТВО
);

SELECT 
    Н_ЛЮДИ.ФАМИЛИЯ
FROM Н_УЧЕНИКИ
    INNER JOIN Н_ПЛАНЫ 
	    ON Н_ПЛАНЫ.ИД = Н_УЧЕНИКИ.ПЛАН_ИД
    INNER JOIN Н_ОТДЕЛЫ 
	    ON Н_ОТДЕЛЫ.ИД = Н_ПЛАНЫ.ОТД_ИД
    INNER JOIN Н_ЛЮДИ 
	    ON Н_ЛЮДИ.ИД = Н_УЧЕНИКИ.ЧЛВК_ИД
WHERE 
    Н_ОТДЕЛЫ.КОРОТКОЕ_ИМЯ = 'КТиУ'
GROUP BY 
    Н_ЛЮДИ.ФАМИЛИЯ
HAVING 
    COUNT(*) = 10;

SELECT 
    Н_ЛЮДИ.ФАМИЛИЯ,
    COUNT(*) AS КОЛИЧЕСТВО_ЛЮДЕЙ_С_ТАКОЙ_ФАМИЛИЕЙ
FROM 
	Н_ЛЮДИ
WHERE 
    Н_ЛЮДИ.ФАМИЛИЯ IN (
        SELECT 
            Н_ЛЮДИ.ФАМИЛИЯ
        FROM 
            Н_УЧЕНИКИ
            INNER JOIN Н_ПЛАНЫ 
	            ON Н_ПЛАНЫ.ИД = Н_УЧЕНИКИ.ПЛАН_ИД
            INNER JOIN Н_ОТДЕЛЫ 
	            ON Н_ОТДЕЛЫ.ИД = Н_ПЛАНЫ.ОТД_ИД
            INNER JOIN Н_ЛЮДИ 
	            ON Н_ЛЮДИ.ИД = Н_УЧЕНИКИ.ЧЛВК_ИД
        WHERE 
            Н_ОТДЕЛЫ.КОРОТКОЕ_ИМЯ = 'КТиУ'
        GROUP BY 
            Н_ЛЮДИ.ФАМИЛИЯ
        HAVING 
            COUNT(*) = 10
    )
GROUP BY 
    Н_ЛЮДИ.ФАМИЛИЯ;


WITH МИН_ВОЗРАСТ AS (
		SELECT DATE_PART('year', AGE(CURRENT_DATE, Н_ЛЮДИ.ДАТА_РОЖДЕНИЯ)) AS ВОЗРАСТ
	FROM Н_УЧЕНИКИ 
		INNER JOIN Н_ЛЮДИ 
			ON Н_ЛЮДИ.ИД = Н_УЧЕНИКИ.ЧЛВК_ИД 
	WHERE 
		ГРУППА = '1100'
		AND DATE_PART('year', AGE(CURRENT_DATE, Н_ЛЮДИ.ДАТА_РОЖДЕНИЯ)) > 20
	GROUP BY 
		ВОЗРАСТ
	ORDER BY 
		ВОЗРАСТ ASC 
	LIMIT 1
)

SELECT
	Н_УЧЕНИКИ.ГРУППА,
	ROUND(AVG(DATE_PART('year', AGE(CURRENT_DATE, Н_ЛЮДИ.ДАТА_РОЖДЕНИЯ)))) AS СР_ВОЗРАСТ
FROM 
    Н_УЧЕНИКИ 
    INNER JOIN Н_ЛЮДИ 
	    ON Н_ЛЮДИ.ИД = Н_УЧЕНИКИ.ЧЛВК_ИД
	CROSS JOIN 
		МИН_ВОЗРАСТ
GROUP BY
    ГРУППА, МИН_ВОЗРАСТ.ВОЗРАСТ
HAVING
	ROUND(AVG(DATE_PART('year', AGE(CURRENT_DATE, Н_ЛЮДИ.ДАТА_РОЖДЕНИЯ)))) = МИН_ВОЗРАСТ.ВОЗРАСТ
ORDER BY
    ГРУППА;

SELECT DISTINCT
	Н_УЧЕНИКИ.ГРУППА,
	Н_ЛЮДИ.ИД,
	Н_ЛЮДИ.ИМЯ,
	Н_ЛЮДИ.ФАМИЛИЯ,
	Н_ЛЮДИ.ОТЧЕСТВО,
	Н_ФОРМЫ_ОБУЧЕНИЯ.НАИМЕНОВАНИЕ,
	Н_ПЛАНЫ.ИД,
	Н_УЧЕНИКИ.СОСТОЯНИЕ
FROM Н_УЧЕНИКИ
	INNER JOIN Н_ПЛАНЫ
		ON Н_ПЛАНЫ.ИД = Н_УЧЕНИКИ.ПЛАН_ИД
	INNER JOIN Н_ЛЮДИ
		ON Н_ЛЮДИ.ИД = Н_УЧЕНИКИ.ЧЛВК_ИД
	INNER JOIN Н_ФОРМЫ_ОБУЧЕНИЯ
		ON Н_ФОРМЫ_ОБУЧЕНИЯ.ИД = Н_ПЛАНЫ.ФО_ИД
WHERE 
	 Н_ПЛАНЫ.ФО_ИД = 3 

	AND EXISTS (
		SELECT 1
		FROM Н_ПЛАНЫ
		WHERE 
			Н_ПЛАНЫ.ИД = Н_УЧЕНИКИ.ПЛАН_ИД 
			AND Н_ПЛАНЫ.УЧЕБНЫЙ_ГОД = '2012/2013'
	)


SELECT 
	группа1.ИД AS ИД_1_ГРУППА,
	группа2.ИД AS ИД_2_ГРУППА,
	группа1.ИМЯ AS ИМЯ,
	группа1.ФАМИЛИЯ AS ФАМИЛИЯ,
	группа1.ОТЧЕСТВО AS ОТЧЕСТВО
FROM
	Н_ЛЮДИ группа1
JOIN 
	Н_ЛЮДИ группа2 ON
	группа1.ИМЯ = группа2.ИМЯ
	AND группа1.ФАМИЛИЯ = группа2.ФАМИЛИЯ
	AND группа1.ОТЧЕСТВО = группа2.ОТЧЕСТВО
	AND группа2.ИД <> группа1.ИД
;


SELECT 
    Н_ЛЮДИ.ФАМИЛИЯ,
    COUNT(*) AS КОЛИЧЕСТВО_ЛЮДЕЙ_С_ТАКОЙ_ФАМИЛИЕЙ
FROM 
	Н_ЛЮДИ
WHERE 
    Н_ЛЮДИ.ФАМИЛИЯ IN (
        SELECT 
            Н_ЛЮДИ.ФАМИЛИЯ
        FROM 
            Н_УЧЕНИКИ
            FULL OUTER JOIN Н_ПЛАНЫ
	            ON Н_УЧЕНИКИ.ПЛАН_ИД = Н_ПЛАНЫ.ИД
            INNER JOIN Н_ОТДЕЛЫ 
	            ON Н_ОТДЕЛЫ.ИД = Н_ПЛАНЫ.ОТД_ИД
            INNER JOIN Н_ЛЮДИ 
	            ON Н_ЛЮДИ.ИД = Н_УЧЕНИКИ.ЧЛВК_ИД
        WHERE 
            Н_ОТДЕЛЫ.КОРОТКОЕ_ИМЯ = 'КТиУ'
            AND Н_ПЛАНЫ.ИД IS NOT NULL
            OR Н_УЧЕНИКИ.ПЛАН_ИД IS NOT NULL
        GROUP BY 
            Н_ЛЮДИ.ФАМИЛИЯ
        HAVING 
            COUNT(*) = 10
    )
GROUP BY 
    Н_ЛЮДИ.ФАМИЛИЯ LIMIT 5;
