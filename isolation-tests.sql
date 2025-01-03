-- Тест для READ COMMITTED (Сеанс 1)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT * FROM sparepart WHERE sparepart_id = 1;
-- Чекаємо, поки Сеанс 2 зробить зміни
SELECT * FROM sparepart WHERE sparepart_id = 1;
COMMIT;

-- Тест для READ COMMITTED (Сеанс 2)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
UPDATE sparepart SET sparepart_name = 'Updated Part' WHERE sparepart_id = 1;
COMMIT;

-- Тест для REPEATABLE READ (Сеанс 1)
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT * FROM sparepart WHERE sparepart_id = 1;
-- Чекаємо, поки Сеанс 2 зробить зміни
SELECT * FROM sparepart WHERE sparepart_id = 1;
COMMIT;

-- Тест для REPEATABLE READ (Сеанс 2)
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
UPDATE sparepart SET sparepart_name = 'Another Update' WHERE sparepart_id = 1;
COMMIT;

-- Тест для SERIALIZABLE (Сеанс 1)
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM sparepart WHERE sparepart_id = 1;
-- Спроба оновити дані
UPDATE sparepart SET sparepart_name = 'Serializable Update' WHERE sparepart_id = 1;
COMMIT;

-- Тест для SERIALIZABLE (Сеанс 2)
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM sparepart WHERE sparepart_id = 1;
-- Спроба оновити ті самі дані
UPDATE sparepart SET sparepart_name = 'Concurrent Update' WHERE sparepart_id = 1;
COMMIT;
