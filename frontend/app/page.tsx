'use client';

import { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { RentalRequest, getRequests, processEmails, formatStatus, getStatusColor } from '@/lib/api';
import RequestCard from '@/components/RequestCard';

const STATUS_FILTERS = [
  { value: '', label: 'Todos os pedidos' },
  { value: 'pending_info', label: 'A aguardar informacao' },
  { value: 'pending_selection', label: 'Por Tratar' },
  { value: 'proposal_sent', label: 'Propostas Enviadas' },
  { value: 'accepted', label: 'Pronto para Confirmar' },
  { value: 'invoiced', label: 'Confirmado' },
  { value: 'cancelled', label: 'Nao confirmado' },
];

const TIME_PERIODS = [
  { value: 'daily', label: 'Hoje' },
  { value: 'weekly', label: 'Esta semana' },
  { value: 'monthly', label: 'Este mes' },
  { value: 'yearly', label: 'Este ano' },
];

export default function Dashboard() {
  const [requests, setRequests] = useState<RentalRequest[]>([]);
  const [allRequests, setAllRequests] = useState<RentalRequest[]>([]);
  const [statusFilter, setStatusFilter] = useState('');
  const [timePeriod, setTimePeriod] = useState('daily');
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadRequests = async () => {
    try {
      setLoading(true);
      const [filtered, all] = await Promise.all([
        getRequests(statusFilter || undefined),
        getRequests(),
      ]);
      setRequests(filtered);
      setAllRequests(all);
      setError(null);
    } catch (e) {
      setError('Failed to load requests');
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRequests();
  }, [statusFilter]);

  // Calculate completed requests for the selected time period
  const getCompletedStats = () => {
    const now = new Date();
    let startDate: Date;

    switch (timePeriod) {
      case 'daily':
        startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        break;
      case 'weekly':
        const dayOfWeek = now.getDay();
        const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
        startDate = new Date(now.getFullYear(), now.getMonth(), diff);
        break;
      case 'monthly':
        startDate = new Date(now.getFullYear(), now.getMonth(), 1);
        break;
      case 'yearly':
        startDate = new Date(now.getFullYear(), 0, 1);
        break;
      default:
        startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    }

    const periodRequests = allRequests.filter(r => {
      const createdAt = new Date(r.created_at);
      return createdAt >= startDate;
    });

    const completed = periodRequests.filter(r => r.status === 'invoiced').length;
    const total = periodRequests.length;

    return { completed, total };
  };

  const completedStats = getCompletedStats();

  const handleProcessEmails = async () => {
    try {
      setProcessing(true);
      const result = await processEmails();
      if (result.processed > 0) {
        toast.success(`${result.processed} novos emails processados`);
      } else {
        toast.info('Nenhum novo email encontrado');
      }
      loadRequests();
    } catch (e) {
      toast.error('Erro ao processar emails');
      console.error(e);
    } finally {
      setProcessing(false);
    }
  };

  // Calculate stats per wireframe
  const stats = {
    porTratar: allRequests.filter(r => r.status === 'pending_selection').length,
    propostasEnviadas: allRequests.filter(r => r.status === 'proposal_sent').length,
    prontoConfirmar: allRequests.filter(r => r.status === 'accepted').length,
    confirmado: allRequests.filter(r => r.status === 'invoiced').length,
    naoConfirmado: allRequests.filter(r => r.status === 'cancelled').length,
  };

  return (
    <div>
      {/* Header with Counter */}
      <div style={{
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        gap: '12px',
        marginBottom: '24px',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          backgroundColor: '#ffffff',
          padding: '12px 20px',
          borderRadius: '12px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          border: '1px solid #e2e8f0',
        }}>
          <span style={{
            fontSize: '14px',
            fontWeight: 600,
            color: '#0f172a',
          }}>
            Pedidos concluidos:{' '}
            <span style={{ color: '#10b981' }}>{completedStats.completed}</span>
            <span style={{ color: '#64748b' }}>/</span>
            <span style={{ color: '#3b82f6' }}>{completedStats.total}</span>
          </span>
          <select
            value={timePeriod}
            onChange={(e) => setTimePeriod(e.target.value)}
            style={{
              padding: '6px 12px',
              borderRadius: '6px',
              border: '1px solid #e2e8f0',
              fontSize: '13px',
              backgroundColor: '#f8fafc',
              color: '#475569',
              cursor: 'pointer',
            }}
          >
            {TIME_PERIODS.map((period) => (
              <option key={period.value} value={period.value}>
                {period.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Stats Cards - 5 cards per wireframe */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(5, 1fr)',
        gap: '16px',
        marginBottom: '32px',
      }}>
        {[
          { label: 'Por Tratar', value: stats.porTratar, color: '#3b82f6', bgColor: '#eff6ff' }, // Blue
          { label: 'Propostas Enviadas', value: stats.propostasEnviadas, color: '#8b5cf6', bgColor: '#f5f3ff' }, // Lilac
          { label: 'Pronto para Confirmar', value: stats.prontoConfirmar, color: '#f59e0b', bgColor: '#fffbeb' }, // Yellow
          { label: 'Confirmado', value: stats.confirmado, color: '#10b981', bgColor: '#ecfdf5' }, // Green
          { label: 'Nao confirmado', value: stats.naoConfirmado, color: '#ef4444', bgColor: '#fef2f2' }, // Red
        ].map((stat, i) => (
          <div key={i} style={{
            backgroundColor: '#ffffff',
            borderRadius: '12px',
            padding: '20px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            border: '1px solid #e2e8f0',
            borderLeft: `4px solid ${stat.color}`,
            transition: 'all 0.2s',
          }}>
            <p style={{
              margin: 0,
              fontSize: '12px',
              color: '#64748b',
              fontWeight: 500,
              marginBottom: '8px',
            }}>
              {stat.label}
            </p>
            <p style={{
              margin: 0,
              fontSize: '28px',
              fontWeight: 700,
              color: stat.color,
              lineHeight: 1,
            }}>
              {stat.value}
            </p>
          </div>
        ))}
      </div>

      {/* Actions Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '24px',
        backgroundColor: '#ffffff',
        padding: '16px 20px',
        borderRadius: '12px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        border: '1px solid #e2e8f0',
      }}>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {STATUS_FILTERS.map((filter) => (
            <button
              key={filter.value}
              onClick={() => setStatusFilter(filter.value)}
              style={{
                padding: '10px 16px',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: 500,
                backgroundColor: statusFilter === filter.value ? '#0f172a' : '#f1f5f9',
                color: statusFilter === filter.value ? 'white' : '#475569',
                transition: 'all 0.2s',
              }}
            >
              {filter.label}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={loadRequests}
            disabled={loading}
            style={{
              padding: '10px 20px',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: 500,
              backgroundColor: '#ffffff',
              color: '#475569',
              transition: 'all 0.2s',
            }}
          >
            Atualizar
          </button>
          <button
            onClick={handleProcessEmails}
            disabled={processing}
            style={{
              padding: '10px 20px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: 600,
              backgroundColor: '#0f172a',
              color: 'white',
              opacity: processing ? 0.7 : 1,
              transition: 'all 0.2s',
            }}
          >
            {processing ? 'A processar...' : 'Verificar emails'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div style={{
          backgroundColor: '#fef2f2',
          color: '#dc2626',
          padding: '16px 20px',
          borderRadius: '12px',
          marginBottom: '20px',
          border: '1px solid #fecaca',
          fontSize: '14px',
        }}>
          {error}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div style={{
          textAlign: 'center',
          padding: '60px',
          color: '#64748b',
          fontSize: '14px',
        }}>
          A carregar pedidos...
        </div>
      )}

      {/* Requests List */}
      {!loading && requests.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '80px 20px',
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          border: '1px solid #e2e8f0',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '16px',
            backgroundColor: '#f1f5f9',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 20px',
          }}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="1.5">
              <rect x="3" y="4" width="18" height="16" rx="2" />
              <path d="M3 8h18" />
              <path d="M8 12h8" />
              <path d="M8 16h4" />
            </svg>
          </div>
          <p style={{ margin: 0, fontSize: '16px', fontWeight: 600, color: '#1e293b' }}>
            Nenhum pedido de aluguer encontrado
          </p>
          <p style={{ margin: '8px 0 0', fontSize: '14px', color: '#64748b' }}>
            Clicar em "Verificar emails" para processar novos pedidos
          </p>
        </div>
      )}

      {!loading && requests.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {requests.map((request) => (
            <RequestCard key={request.id} request={request} />
          ))}
        </div>
      )}
    </div>
  );
}
