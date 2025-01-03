-- Створення B-tree індексу для пошуку за назвою запчастини
CREATE INDEX idx_sparepart_name ON sparepart USING btree (sparepart_name);

-- Створення GIN індексу для повнотекстового пошуку в інформації про запчастини
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_sparepart_info_gin ON sparepart USING gin (sparepart_info gin_trgm_ops);

-- Генерація тестових даних
INSERT INTO sparepart (sparepart_name, sparepart_info)
SELECT 
    'Part ' || i::text,
    'Description for part ' || i::text || ' with details about manufacturing and specifications'
FROM generate_series(1, 10000) i;

-- Тест 1: Пошук за точною назвою (використовує B-tree індекс)
EXPLAIN ANALYZE
SELECT * FROM sparepart
WHERE sparepart_name = 'Part 100';

-- Тест 2: Пошук за частковим співпадінням в інформації (використовує GIN індекс)
EXPLAIN ANALYZE
SELECT * FROM sparepart
WHERE sparepart_info LIKE '%manufacturing%';

-- Тест 3: Сортування за назвою (використовує B-tree індекс)
EXPLAIN ANALYZE
SELECT * FROM sparepart
ORDER BY sparepart_name
LIMIT 100;

-- Тест 4: Повнотекстовий пошук у інформації (використовує GIN індекс)
EXPLAIN ANALYZE
SELECT * FROM sparepart
WHERE sparepart_info ILIKE '%specifications%';
