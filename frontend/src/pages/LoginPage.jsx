import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Alert, Button, Card, Form } from 'react-bootstrap';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post('/auth/login', { email, password });
      login(data.access_token, data.user);
      navigate('/');
    } catch {
      setError('Invalid credentials.');
    }
  };

  return (
    <Card className="mx-auto p-4" style={{ maxWidth: 460 }}>
      <h3>Login</h3>
      {error && <Alert variant="danger">{error}</Alert>}
      <Form onSubmit={submit}>
        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control value={email} onChange={(e) => setEmail(e.target.value)} required />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </Form.Group>
        <Button type="submit">Sign In</Button>
      </Form>
    </Card>
  );
}
