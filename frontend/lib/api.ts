const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface RentalRequest {
  id: string;
  status: 'pending_info' | 'pending_selection' | 'proposal_sent' | 'accepted' | 'invoiced' | 'cancelled';
  client_name: string | null;
  client_email: string;
  client_vat: string | null;
  client_phone: string | null;
  pickup_date: string | null;
  return_date: string | null;
  pickup_location: string | null;
  return_location: string | null;
  vehicle_type: string | null;
  special_requests: string | null;
  driver_name: string | null;
  artist_project_event: string | null;
  destination_cities: string | null;
  selected_partner_id: string | "";
  selected_vehicle_id: string | null;
  selected_partner_name: string | null;
  selected_vehicle_description: string | null;
  cost_price: number | null;
  price: number | null;
  original_email_subject: string | null;
  internal_notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface Partner {
  id: string;
  name: string;
  contact_email: string | null;
  notes: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Vehicle {
  id: string;
  partner_id: string;
  category: string;
  group_code: string;
  description: string;
  price_1_3_days: number | null;
  price_4_6_days: number | null;
  price_7_29_days: number | null;
  price_monthly: number | null;
  franchise: number | null;
  min_age: number | null;
  license_years: number | null;
  notes: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface VehicleWithPartner extends Vehicle {
  partner: Partner;
}

export async function getRequests(status?: string): Promise<RentalRequest[]> {
  const url = status
    ? `${API_URL}/api/requests?status=${status}`
    : `${API_URL}/api/requests`;

  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch requests');
  return res.json();
}

export async function getRequest(id: string): Promise<RentalRequest> {
  const res = await fetch(`${API_URL}/api/requests/${id}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch request');
  return res.json();
}

export async function getPartners(): Promise<Partner[]> {
  const res = await fetch(`${API_URL}/api/partners`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch partners');
  return res.json();
}

export async function getPartnerCategories(partnerId: number): Promise<string[]> {
  const res = await fetch(`${API_URL}/api/partners/${partnerId}/categories`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function getPartnerVehicles(partnerId: string, category?: string): Promise<Vehicle[]> {
  const url = category
    ? `${API_URL}/api/partners/${partnerId}/vehicles?category=${encodeURIComponent(category)}`
    : `${API_URL}/api/partners/${partnerId}/vehicles`;
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch vehicles');
  return res.json();
}

export async function selectPartner(
  requestId: string,
  partnerId: string,
  vehicleId: string,
  costPrice: number,
  price: number
): Promise<void> {
  const res = await fetch(`${API_URL}/api/requests/${requestId}/select-partner`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ partner_id: partnerId, vehicle_id: vehicleId, cost_price: costPrice, price }),
  });
  if (!res.ok) throw new Error('Failed to select partner');
}

export async function sendProposal(requestId: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/requests/${requestId}/send-proposal`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to send proposal');
}

export async function sendPartnerRequest(requestId: string): Promise<{ message: string }> {
  const res = await fetch(`${API_URL}/api/requests/${requestId}/send-partner-request`, {
    method: 'POST',
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Failed to send partner request' }));
    throw new Error(error.detail || 'Failed to send partner request');
  }
  return res.json();
}

export async function markAccepted(requestId: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/requests/${requestId}/mark-accepted`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to mark as accepted');
}

export async function confirmBooking(requestId: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/requests/${requestId}/confirm`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to confirm booking');
}

export async function updateNotes(requestId: string, notes: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/requests/${requestId}/notes`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notes }),
  });
  if (!res.ok) throw new Error('Failed to update notes');
}

export async function updatePartnerNotes(partnerId: string, notes: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/partners/${partnerId}/notes`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notes }),
  });
  if (!res.ok) throw new Error('Failed to update partner notes');
}

export async function getPartner(partnerId: string): Promise<Partner & { vehicles: Vehicle[] }> {
  const res = await fetch(`${API_URL}/api/partners/${partnerId}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch partner');
  return res.json();
}

export async function processEmails(): Promise<{ processed: number }> {
  const res = await fetch(`${API_URL}/api/process-emails`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to process emails');
  return res.json();
}

export function formatStatus(status: string): string {
  const statusMap: Record<string, string> = {
    pending_info: 'A aguardar informação',
    pending_selection: 'Selecionar parceiro',
    proposal_sent: 'Proposta enviada',
    accepted: 'Aceite',
    invoiced: 'Faturado',
    cancelled: 'Cancelado',
  };
  return statusMap[status] || status;
}

export function getStatusColor(status: string): string {
  const colorMap: Record<string, string> = {
    pending_info: '#ffc107',
    pending_selection: '#17a2b8',
    proposal_sent: '#6c757d',
    accepted: '#28a745',
    invoiced: '#007bff',
    cancelled: '#dc3545',
  };
  return colorMap[status] || '#6c757d';
}

export async function getAllCategories(): Promise<string[]> {
  const res = await fetch(`${API_URL}/api/categories`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function getPartnersByCategory(category: string): Promise<Partner[]> {
  const res = await fetch(`${API_URL}/api/categories/${encodeURIComponent(category)}/partners`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch partners for category');
  return res.json();
}
