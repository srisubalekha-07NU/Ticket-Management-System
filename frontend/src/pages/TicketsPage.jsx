import { useEffect, useState } from 'react';
import { Badge, Button, Card, Form, Table } from 'react-bootstrap';
import api from '../services/api';

const priorities = ['Low', 'Medium', 'High', 'Critical'];

export default function TicketsPage() {
  const [tickets, setTickets] = useState([]);
  const [form, setForm] = useState({ project_name: '', subject: '', description: '', priority: 'Medium', estimated_hours: 1, start_at: '', end_at: '', received_department: '' });

  const load = async () => {
    const { data } = await api.get('/tickets');
    setTickets(data);
  };

  useEffect(() => { load(); }, []);

  const create = async (e) => {
    e.preventDefault();
    await api.post('/tickets', { ...form, assignments: [], sub_tickets: [] });
    setForm({ project_name: '', subject: '', description: '', priority: 'Medium', estimated_hours: 1, start_at: '', end_at: '', received_department: '' });
    load();
  };

  return (
    <>
      <Card className="p-3 mb-4">
        <h4>Create Ticket</h4>
        <Form onSubmit={create} className="row g-2">
          <Form.Control className="col" placeholder="Project" value={form.project_name} onChange={(e) => setForm({ ...form, project_name: e.target.value })} required />
          <Form.Control className="col" placeholder="Subject" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} required />
          <Form.Select className="col" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>{priorities.map((p) => <option key={p}>{p}</option>)}</Form.Select>
          <Button className="col-auto" type="submit">Create</Button>
        </Form>
      </Card>

      <Card className="p-3">
        <h4>Tickets</h4>
        <Table responsive>
          <thead><tr><th>ID</th><th>Project</th><th>Subject</th><th>Priority</th><th>Status</th></tr></thead>
          <tbody>
            {tickets.map((t) => (
              <tr key={t.id}>
                <td>{t.id}</td><td>{t.project}</td><td>{t.subject}</td><td><Badge bg="secondary">{t.priority}</Badge></td><td>{t.status}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Card>
    </>
  );
}
