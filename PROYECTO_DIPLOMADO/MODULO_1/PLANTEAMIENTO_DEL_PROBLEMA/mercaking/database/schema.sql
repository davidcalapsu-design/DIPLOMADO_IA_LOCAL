-- ==============================================================================
-- MercaKing — Esquema MySQL (phpMyAdmin)
-- Adaptado de supabase_schema.sql (PostgreSQL) a MySQL
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS mercaking
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mercaking;

-- Tenants (minimercados / inquilinos)
CREATE TABLE IF NOT EXISTS tenants (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    nit VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(150),
    address VARCHAR(255),
    city VARCHAR(100) DEFAULT 'Bogotá',
    currency VARCHAR(10) DEFAULT 'COP',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Perfiles de usuario
CREATE TABLE IF NOT EXISTS profiles (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    avatar_url TEXT,
    system_role ENUM('platform_admin','store_owner','store_admin','cashier','inventory_manager') NOT NULL DEFAULT 'cashier',
    password_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Asignación usuario - tenant (multi-inquilino)
CREATE TABLE IF NOT EXISTS user_tenants (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    tenant_id CHAR(36) NOT NULL,
    role ENUM('platform_admin','store_owner','store_admin','cashier','inventory_manager') NOT NULL DEFAULT 'cashier',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_tenant (user_id, tenant_id),
    FOREIGN KEY (user_id) REFERENCES profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- Categorías
CREATE TABLE IF NOT EXISTS categories (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_tenant_category (tenant_id, name),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- Proveedores
CREATE TABLE IF NOT EXISTS suppliers (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    nit_rut VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(150),
    address VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- Productos
CREATE TABLE IF NOT EXISTS products (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    category_id CHAR(36),
    supplier_id CHAR(36),
    name VARCHAR(255) NOT NULL,
    barcode VARCHAR(100),
    sku VARCHAR(100),
    description TEXT,
    purchase_price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    sale_price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    current_stock DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    min_stock DECIMAL(12,2) NOT NULL DEFAULT 5.00,
    unit_measure VARCHAR(50) NOT NULL DEFAULT 'unidad',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_tenant_barcode (tenant_id, barcode),
    UNIQUE KEY uq_tenant_sku (tenant_id, sku),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
);

-- Movimientos de inventario (Kardex)
CREATE TABLE IF NOT EXISTS inventory_movements (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    user_id CHAR(36),
    movement_type ENUM('entry','exit','adjustment','sale') NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    previous_stock DECIMAL(12,2) NOT NULL,
    new_stock DECIMAL(12,2) NOT NULL,
    reason VARCHAR(255) NOT NULL,
    reference_id CHAR(36),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES profiles(id) ON DELETE SET NULL
);

-- Ventas (cabecera)
CREATE TABLE IF NOT EXISTS sales (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    user_id CHAR(36),
    sale_number VARCHAR(50) NOT NULL,
    customer_name VARCHAR(150) NOT NULL DEFAULT 'Consumidor Final',
    customer_doc VARCHAR(50),
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    tax DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    discount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    total DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    payment_method ENUM('cash','card','transfer','other') NOT NULL DEFAULT 'cash',
    amount_paid DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    change_given DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    status ENUM('completed','cancelled') NOT NULL DEFAULT 'completed',
    notes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_tenant_sale_number (tenant_id, sale_number),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES profiles(id) ON DELETE SET NULL
);

-- Detalle de venta
CREATE TABLE IF NOT EXISTS sale_items (
    id CHAR(36) PRIMARY KEY,
    sale_id CHAR(36) NOT NULL,
    tenant_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- Auditoría
CREATE TABLE IF NOT EXISTS audit_logs (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36),
    user_id CHAR(36),
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100) NOT NULL,
    entity_id CHAR(36),
    details JSON,
    ip_address VARCHAR(50),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES profiles(id) ON DELETE SET NULL
);

-- Índices de rendimiento
CREATE INDEX idx_products_tenant ON products(tenant_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_barcode ON products(barcode);
CREATE INDEX idx_sales_tenant_date ON sales(tenant_id, created_at);
CREATE INDEX idx_sale_items_sale ON sale_items(sale_id);
CREATE INDEX idx_inventory_movements_prod ON inventory_movements(tenant_id, product_id, created_at);
CREATE INDEX idx_audit_logs_tenant ON audit_logs(tenant_id, created_at);
CREATE INDEX idx_user_tenants_lookup ON user_tenants(user_id, tenant_id);
