import { useEffect, useState } from 'react';
import { Button, Card, Form } from 'react-bootstrap';
import api from '../services/api';

export default function WorklogsPage() {
  const [summary, setSummary] = useState(null);
  const [form, setForm] = useState({ ticket_id: '', work_date: '', hours_spent: '', activity_id: '', comments: '' });

  const loadSummary = async () => {
    const { data } = await api.get('/worklogs/summary/monthly');
    setSummary(data);
  };
  useEffect(() => { loadSummary(); }, []);

  const submit = async (e) => {
    e.preventDefault();
    await api.post('/worklogs', form);
    loadSummary();
  };

  return (
    <>
      <Card className="p-3 mb-3">
        <h4>Add Work Log</h4>
        <Form onSubmit={submit} className="row g-2">
          <Form.Control className="col" placeholder="Ticket ID" value={form.ticket_id} onChange={(e) => setForm({ ...form, ticket_id: e.target.value })} required />
          <Form.Control className="col" type="date" value={form.work_date} onChange={(e) => setForm({ ...form, work_date: e.target.value })} required />
          <Form.Control className="col" type="number" step="0.25" placeholder="Hours" value={form.hours_spent} onChange={(e) => setForm({ ...form, hours_spent: e.target.value })} required />
          <Form.Control className="col" placeholder="Activity ID" value={form.activity_id} onChange={(e) => setForm({ ...form, activity_id: e.target.value })} required />
          <Button className="col-auto" type="submit">Save</Button>
        </Form>
      </Card>
      {summary && <Card className="p-3">Target: {summary.target_hours} | Completed: {summary.completed_hours} | Missing: {summary.missing_hours} | Overlogged: {summary.overlogged_hours}</Card>}
    </>
  );
}
