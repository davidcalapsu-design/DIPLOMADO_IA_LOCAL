-- ==============================================================================
-- MercaKing — Datos semilla (demo) para MySQL
-- ==============================================================================
USE mercaking;

-- Tenants de prueba
INSERT INTO tenants (id, name, slug, nit, phone, email, address, city) VALUES
('a0000000-0000-0000-0000-000000000001', 'Minimarket El Ahorro', 'el-ahorro', '900.123.456-1', '3101234567', 'contacto@elahorro.com', 'Calle 45 # 12-34', 'Bogotá'),
('a0000000-0000-0000-0000-000000000002', 'Minimarket San Jorge', 'san-jorge', '900.987.654-2', '3209876543', 'ventas@sanjorge.com', 'Carrera 15 # 78-90', 'Medellín')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Perfiles demo
INSERT INTO profiles (id, email, full_name, system_role, password_hash, is_active) VALUES
('u0000000-0000-0000-0000-000000000001', 'admin@plataforma.com', 'Alejandro Morales', 'platform_admin', '$2b$12$placeholder', TRUE),
('u0000000-0000-0000-0000-000000000002', 'dueno@elahorro.com', 'Carlos Andrés Gómez', 'store_owner', '$2b$12$placeholder', TRUE),
('u0000000-0000-0000-0000-000000000003', 'cajero@elahorro.com', 'Laura Sofía Restrepo', 'cashier', '$2b$12$placeholder', TRUE)
ON DUPLICATE KEY UPDATE email = VALUES(email);

-- Asignación tenant (El Ahorro)
INSERT INTO user_tenants (id, user_id, tenant_id, role) VALUES
('ut000000-0000-0000-0000-000000000001', 'u0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'store_owner'),
('ut000000-0000-0000-0000-000000000002', 'u0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'cashier')
ON DUPLICATE KEY UPDATE role = VALUES(role);

-- Categorías (El Ahorro)
INSERT INTO categories (id, tenant_id, name, description) VALUES
('c1000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'Lácteos y Huevos', 'Leche, quesos, yogures'),
('c1000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Bebidas y Refrescos', 'Gaseosas, jugos, aguas'),
('c1000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'Abarrotes y Granos', 'Arroz, aceite, azúcar, pastas')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Categorías (San Jorge)
INSERT INTO categories (id, tenant_id, name, description) VALUES
('c2000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'Panadería y Café', 'Panes frescos y cafés'),
('c2000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'Carnes y Embutidos', 'Jamones y carnes frías')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Proveedores (El Ahorro)
INSERT INTO suppliers (id, tenant_id, name, contact_name, nit_rut, phone, email, address) VALUES
('s1000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'Distribuidora Lácteos del Campo', 'Carlos Gómez', '890.111.222-3', '3114445566', 'pedidos@lacteosdelcampo.com', 'Zona Industrial Calle 13'),
('s1000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Bebidas y Refrescos Nacionales', 'Mariana Torres', '860.333.444-5', '3157778899', 'ventas@bebidasnac.com', 'Av. Boyacá # 68-20')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Productos (El Ahorro)
INSERT INTO products (id, tenant_id, category_id, supplier_id, name, barcode, sku, purchase_price, sale_price, current_stock, min_stock, unit_measure) VALUES
('p1000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'c1000000-0000-0000-0000-000000000001', 's1000000-0000-0000-0000-000000000001', 'Leche Entera 1000ml', '770123400001', 'LEC-001', 3200, 4200, 45, 10, 'unidad'),
('p1000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'c1000000-0000-0000-0000-000000000001', 's1000000-0000-0000-0000-000000000001', 'Queso Campesino 500g', '770123400002', 'QUE-002', 6500, 8900, 4, 8, 'unidad'),
('p1000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'c1000000-0000-0000-0000-000000000002', 's1000000-0000-0000-0000-000000000002', 'Gaseosa Coca-Cola 1.5L', '770123400003', 'GAS-003', 4500, 6000, 28, 12, 'unidad'),
('p1000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000001', 'c1000000-0000-0000-0000-000000000003', NULL, 'Arroz Diana Blanco 1kg', '770123400004', 'ARR-004', 3800, 4800, 60, 15, 'unidad'),
('p1000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000001', 'c1000000-0000-0000-0000-000000000003', NULL, 'Aceite Premier Vegetal 900ml', '770123400005', 'ACE-005', 7200, 9500, 2, 6, 'unidad')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Productos (San Jorge)
INSERT INTO products (id, tenant_id, category_id, name, barcode, sku, purchase_price, sale_price, current_stock, min_stock, unit_measure) VALUES
('p2000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'c2000000-0000-0000-0000-000000000001', 'Pan Tajado Bimbo Blanco', '770987600001', 'PAN-101', 4200, 5800, 18, 5, 'unidad'),
('p2000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'c2000000-0000-0000-0000-000000000002', 'Jamón Pietrán Pollo 230g', '770987600002', 'JAM-102', 7800, 10500, 3, 6, 'unidad')
ON DUPLICATE KEY UPDATE name = VALUES(name);
