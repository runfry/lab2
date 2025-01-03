-- Створення функції тригера
CREATE OR REPLACE FUNCTION update_warehouse_spareparts()
RETURNS TRIGGER AS $$
DECLARE
    total_parts INTEGER;
BEGIN
    -- Якщо це вставка або оновлення в таблиці warehouse_sparepart
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        -- Підрахунок загальної кількості різних запчастин для складу
        SELECT COUNT(DISTINCT sparepart_id) 
        INTO total_parts 
        FROM warehouse_sparepart 
        WHERE warehouse_id = NEW.warehouse_id;
        
        -- Оновлення кількості доступних запчастин у складі
        UPDATE warehouse 
        SET available_spareparts = total_parts 
        WHERE warehouse_id = NEW.warehouse_id;
        
        RAISE NOTICE 'Updated warehouse % with % available spareparts', 
                    NEW.warehouse_id, total_parts;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Створення тригера
CREATE TRIGGER trg_update_warehouse_spareparts
AFTER INSERT OR UPDATE ON warehouse_sparepart
FOR EACH ROW
EXECUTE FUNCTION update_warehouse_spareparts();

-- Тестування тригера
-- Вставка нового зв'язку склад-запчастина
INSERT INTO warehouse_sparepart (warehouse_id, sparepart_id) 
VALUES (1, 1);

-- Оновлення існуючого зв'язку
UPDATE warehouse_sparepart 
SET sparepart_id = 2 
WHERE warehouse_id = 1 AND sparepart_id = 1;
