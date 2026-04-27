'use client';

import { RentalRequest } from '@/lib/api';
import Link from 'next/link';

interface RequestCardProps {
  request: RentalRequest;
}

export default function RequestCard({ request }: RequestCardProps) {
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('pt-PT', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };

  // Card colors per wireframe:
  // Por Tratar (Blue) - pending_selection
  // Propostas Enviadas (Lilac) - proposal_sent
  // Pronto para Confirmar (Yellow) - accepted
  // Confirmado (Green) - invoiced
  // Não confirmado (Red) - cancelled
  const statusColorMap: Record<string, { bg: string; text: string; border: string; cardBorder: string; cardBg: string }> = {
    pending_info: { bg: '#fef3c7', text: '#92400e', border: '#fcd34d', cardBorder: '#fcd34d', cardBg: '#fffbeb' },
    pending_selection: { bg: '#dbeafe', text: '#1d4ed8', border: '#60a5fa', cardBorder: '#3b82f6', cardBg: '#eff6ff' }, // Blue
    proposal_sent: { bg: '#f3e8ff', text: '#7c3aed', border: '#c4b5fd', cardBorder: '#8b5cf6', cardBg: '#faf5ff' }, // Lilac
    accepted: { bg: '#fef3c7', text: '#b45309', border: '#fcd34d', cardBorder: '#f59e0b', cardBg: '#fffbeb' }, // Yellow
    invoiced: { bg: '#d1fae5', text: '#047857', border: '#34d399', cardBorder: '#10b981', cardBg: '#ecfdf5' }, // Green
    cancelled: { bg: '#fee2e2', text: '#dc2626', border: '#f87171', cardBorder: '#ef4444', cardBg: '#fef2f2' }, // Red
  };

  // Status labels per wireframe
  const statusLabels: Record<string, string> = {
    pending_info: 'A aguardar informacao',
    pending_selection: 'Por Tratar',
    proposal_sent: 'Propostas Enviadas',
    accepted: 'Pronto para Confirmar',
    invoiced: 'Confirmado',
    cancelled: 'Nao confirmado',
  };

  const statusStyle = statusColorMap[request.status] || { bg: '#f1f5f9', text: '#475569', border: '#cbd5e1', cardBorder: '#e2e8f0', cardBg: '#ffffff' };
  const statusLabel = statusLabels[request.status] || request.status;

  return (
    <Link href={`/request/${request.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        padding: '20px 24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        border: '1px solid #e2e8f0',
        cursor: 'pointer',
        transition: 'all 0.2s',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          marginBottom: '16px',
        }}>
          <div>
            <h3 style={{
              margin: '0 0 4px 0',
              fontSize: '16px',
              fontWeight: 600,
              color: '#0f172a',
            }}>
              {request.client_name || request.client_email}
            </h3>
            <p style={{
              margin: 0,
              fontSize: '13px',
              color: '#64748b',
            }}>
              {request.client_email}
            </p>
          </div>
          <span style={{
            backgroundColor: statusStyle.bg,
            color: statusStyle.text,
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '12px',
            fontWeight: 600,
            border: `1px solid ${statusStyle.border}`,
          }}>
            {statusLabel}
          </span>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '20px',
          padding: '16px 0',
          borderTop: '1px solid #f1f5f9',
          borderBottom: '1px solid #f1f5f9',
        }}>
          <div>
            <span style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Levantamento
            </span>
            <p style={{
              margin: '6px 0 0',
              fontSize: '14px',
              fontWeight: 600,
              color: '#1e293b',
            }}>
              {formatDate(request.pickup_date)}
            </p>
            <p style={{
              margin: '2px 0 0',
              fontSize: '13px',
              color: '#64748b',
            }}>
              {request.pickup_location || 'N/A'}
            </p>
          </div>

          <div>
            <span style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Devolucao
            </span>
            <p style={{
              margin: '6px 0 0',
              fontSize: '14px',
              fontWeight: 600,
              color: '#1e293b',
            }}>
              {formatDate(request.return_date)}
            </p>
            <p style={{
              margin: '2px 0 0',
              fontSize: '13px',
              color: '#64748b',
            }}>
              {request.return_location || request.pickup_location || 'N/A'}
            </p>
          </div>

          <div>
            <span style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Veiculo
            </span>
            <p style={{
              margin: '6px 0 0',
              fontSize: '14px',
              fontWeight: 600,
              color: '#1e293b',
            }}>
              {request.vehicle_type?.replace(/_/g, ' ') || 'Nao especificado'}
            </p>
            {request.price && (
              <p style={{
                margin: '2px 0 0',
                fontSize: '14px',
                color: '#10b981',
                fontWeight: 700,
              }}>
                {request.price.toFixed(2)}
              </p>
            )}
          </div>
        </div>

        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginTop: '16px',
        }}>
          {request.selected_partner_name ? (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}>
              <span style={{
                fontSize: '12px',
                color: '#64748b',
              }}>
                Parceiro:
              </span>
              <span style={{
                fontSize: '13px',
                fontWeight: 600,
                color: '#0f172a',
                backgroundColor: '#f1f5f9',
                padding: '4px 10px',
                borderRadius: '6px',
              }}>
                {request.selected_partner_name}
              </span>
            </div>
          ) : (
            <div />
          )}
          <span style={{
            fontSize: '12px',
            color: '#94a3b8',
          }}>
            Criado: {new Date(request.created_at).toLocaleString('pt-PT')}
          </span>
        </div>
      </div>
    </Link>
  );
}
