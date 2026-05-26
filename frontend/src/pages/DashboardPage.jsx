import { Card, Col, Row } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

export default function DashboardPage() {
  const { user } = useAuth();
  const managerView = ['Manager', 'Admin'].includes(user?.role);
  return (
    <>
      <h2 className="mb-3">{managerView ? 'Manager' : 'Employee'} Dashboard</h2>
      <Row className="g-3">
        <Col md={4}><Card className="p-3">Assigned Tickets</Card></Col>
        <Col md={4}><Card className="p-3">Pending Tasks</Card></Col>
        <Col md={4}><Card className="p-3">Monthly Logged Hours</Card></Col>
        {managerView && <Col md={4}><Card className="p-3">Team Utilization</Card></Col>}
        {managerView && <Col md={4}><Card className="p-3">Invoice Summary</Card></Col>}
      </Row>
    </>
  );
}
