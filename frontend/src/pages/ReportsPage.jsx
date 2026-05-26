import { useState } from 'react';
import { Button, Card } from 'react-bootstrap';

export default function ReportsPage() {
  const [base] = useState('/api/reports/monthly');

  return (
    <Card className="p-3">
      <h4>Manager Reports</h4>
      <p>Download monthly reports:</p>
      <div className="d-flex gap-2">
        <Button as="a" href={`${base}?format=json`} target="_blank">JSON</Button>
        <Button as="a" href={`${base}?format=csv`} target="_blank" variant="success">CSV</Button>
        <Button as="a" href={`${base}?format=xlsx`} target="_blank" variant="warning">XLSX</Button>
      </div>
    </Card>
  );
}
