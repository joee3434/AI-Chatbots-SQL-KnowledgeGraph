INSERT INTO locations (name, city, is_active) VALUES
('Main Warehouse', 'Cairo', 1),
('Branch Store', 'Alexandria', 1),
('Old Storage', 'Giza', 0);

INSERT INTO vendors (name, contact_email, is_active) VALUES
('TechVendor Co', 'sales@techvendor.example', 1),
('OfficeSupply Ltd', 'info@officesupply.example', 1),
('LegacyVendor', 'legacy@vendor.example', 0);

INSERT INTO assets (asset_tag, name, category, status, location_id, vendor_id, quantity, is_active) VALUES
('AST-1001', 'Dell Laptop', 'Electronics', 'InService', 1, 1, 15, 1),
('AST-1002', 'HP Printer', 'Electronics', 'InRepair', 1, 2, 3, 1),
('AST-1003', 'Cisco Switch', 'Networking', 'Reserved', 2, 1, 6, 1),
('AST-1004', 'Old Monitor', 'Electronics', 'Retired', 3, 3, 20, 0),
('AST-1005', 'Disposed Router', 'Networking', 'Disposed', 3, 3, 2, 0);
