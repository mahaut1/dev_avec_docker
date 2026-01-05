-- Création de la nouvelle table students
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    specialite VARCHAR(100) NOT NULL,
    annee INTEGER
);

-- Insertion de quelques données de test
INSERT INTO students (nom, specialite, annee) VALUES
('Alice Dupont', 'DevOps', 2),
('Bob Martin', 'Cybersécurité', 2),
('Charlie Leclerc', 'DevOps', 2),
('David Bernard', 'Data Science', 1),
('Eve Moreau', 'Développement web', 5),
('Frank Dubois', 'Intelligence Artificielle', 3)

ON CONFLICT (id) DO NOTHING;