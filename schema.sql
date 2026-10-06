CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('citizen', 'admin', 'worker');
CREATE TYPE waste_category AS ENUM ('Plastic', 'Paper', 'Cardboard', 'Glass', 'Metal', 'Organic', 'E-Waste', 'Mixed Waste', 'Unknown');
CREATE TYPE report_status AS ENUM ('pending', 'verified', 'assigned', 'in_progress', 'resolved', 'rejected', 'manual_verification');
CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE severity_level AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed', 'failed');

CREATE TABLE wards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ward_number VARCHAR(50) UNIQUE NOT NULL,
    ward_name VARCHAR(255) NOT NULL,
    zone VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role user_role DEFAULT 'citizen',
    ward_id UUID REFERENCES wards(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE waste_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    ward_id UUID REFERENCES wards(id),
    image_url TEXT NOT NULL,
    description TEXT,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    waste_type waste_category DEFAULT 'Unknown',
    confidence DECIMAL(5, 4),
    severity severity_level DEFAULT 'low',
    priority priority_level DEFAULT 'low',
    status report_status DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE ai_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id UUID REFERENCES waste_reports(id) ON DELETE CASCADE,
    model_name VARCHAR(100) NOT NULL,
    predicted_class waste_category NOT NULL,
    confidence DECIMAL(5, 4) NOT NULL,
    severity_score DECIMAL(5, 4),
    recommendation TEXT,
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE hotspots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ward_id UUID REFERENCES wards(id),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    report_count INTEGER DEFAULT 1,
    severity_level severity_level DEFAULT 'low',
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
