import unittest
from flask_testing import TestCase
from pymongo import MongoClient

# Initialisez une instance du client MongoDB
client = MongoClient('mongodb://localhost:27017')

# Sélectionnez la base de données
db = client['nom_de_votre_base_de_donnees']


class IntegrationTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Utilisez une base de données distincte pour les tests
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_creation_compte_utilisateur(self):
        # Créez un utilisateur
        user_data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'password123'
        }
        response = self.client.post('/register', data=user_data, follow_redirects=True)
        
        # Vérifiez que l'utilisateur est créé dans la base de données
        user = db.users.find_one({'username': 'john'})
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'john@example.com')
        print("Test de création de compte utilisateur réussi !")

    def test_modification_informations_profil(self):
        # Créez un utilisateur
        user_data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'password123'
        }
        response = self.client.post('/register', data=user_data, follow_redirects=True)

        # Modifiez les informations de profil de l'utilisateur
        updated_user_data = {
            'email': 'newemail@example.com'
        }
        response = self.client.post('/profile', data=updated_user_data, follow_redirects=True)

        # Vérifiez que les informations de l'utilisateur sont mises à jour dans la base de données
        user = User.query.filter_by(username='john').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newemail@example.com')
        print("Test de modification des informations de profil réussi !")

    def test_suppression_compte_utilisateur(self):
        # Créez un utilisateur
        user_data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'password123'
        }
        response = self.client.post('/register', data=user_data, follow_redirects=True)

        # Supprimez le compte de l'utilisateur
        response = self.client.post('/delete', follow_redirects=True)

        # Vérifiez que l'utilisateur est supprimé de la base de données
        user = User.query.filter_by(username='john').first()
        self.assertIsNone(user)
        print("Test de suppression de compte utilisateur réussi !")

if __name__ == '__main__':
    unittest.main()
