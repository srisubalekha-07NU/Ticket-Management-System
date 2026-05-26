import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

export default function NavigationBar() {
  const { user, token, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Ticket System</Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse>
          {token && (
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/tickets">Tickets</Nav.Link>
              <Nav.Link as={Link} to="/worklogs">Work Logs</Nav.Link>
              {['Manager', 'Admin'].includes(user?.role) && (
                <Nav.Link as={Link} to="/reports">Reports</Nav.Link>
              )}
            </Nav>
          )}
          <Nav className="ms-auto align-items-center gap-2">
            {user && <span className="text-light small">{user.name} ({user.role})</span>}
            {token ? (
              <Button size="sm" variant="outline-light" onClick={() => { logout(); navigate('/login'); }}>
                Logout
              </Button>
            ) : (
              <Nav.Link as={Link} to="/login">Login</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
