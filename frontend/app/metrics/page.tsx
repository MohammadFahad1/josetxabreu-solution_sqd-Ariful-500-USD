'use client';

import { useEffect, useState } from 'react';
import { RentalRequest, getRequests } from '@/lib/api';

export default function MetricsPage() {
  const [requests, setRequests] = useState<RentalRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [timePeriod, setTimePeriod] = useState<'all' | 'month' | 'week'>('all');

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getRequests();
        setRequests(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  // Filter by time period
  const getFilteredRequests = () => {
    if (timePeriod === 'all') return requests;

    const now = new Date();
    let startDate: Date;

    if (timePeriod === 'week') {
      const dayOfWeek = now.getDay();
      const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
      startDate = new Date(now.getFullYear(), now.getMonth(), diff);
    } else {
      startDate = new Date(now.getFullYear(), now.getMonth(), 1);
    }

    return requests.filter(r => new Date(r.created_at) >= startDate);
  };

  const filteredRequests = getFilteredRequests();

  // Calculate metrics
  const metrics = {
    total: filteredRequests.length,
    byStatus: {
      pending_selection: filteredRequests.filter(r => r.status === 'pending_selection').length,
      proposal_sent: filteredRequests.filter(r => r.status === 'proposal_sent').length,
      accepted: filteredRequests.filter(r => r.status === 'accepted').length,
      invoiced: filteredRequests.filter(r => r.status === 'invoiced').length,
      cancelled: filteredRequests.filter(r => r.status === 'cancelled').length,
    },
    revenue: filteredRequests
      .filter(r => r.status === 'invoiced' && r.price)
      .reduce((sum, r) => sum + (r.price || 0), 0),
    cost: filteredRequests
      .filter(r => r.status === 'invoiced' && r.cost_price)
      .reduce((sum, r) => sum + (r.cost_price || 0), 0),
    profit: filteredRequests
      .filter(r => r.status === 'invoiced' && r.price && r.cost_price)
      .reduce((sum, r) => sum + ((r.price || 0) - (r.cost_price || 0)), 0),
    conversionRate: filteredRequests.length > 0
      ? (filteredRequests.filter(r => r.status === 'invoiced').length / filteredRequests.length * 100)
      : 0,
  };

  const avgMargin = metrics.revenue > 0 ? (metrics.profit / metrics.revenue * 100) : 0;

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '80px', color: '#64748b' }}>
        A carregar metricas...
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '32px',
      }}>
        <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 700, color: '#0f172a' }}>
          Metricas
        </h1>
        <div style={{ display: 'flex', gap: '8px' }}>
          {[
            { value: 'week', label: 'Esta Semana' },
            { value: 'month', label: 'Este Mes' },
            { value: 'all', label: 'Tudo' },
          ].map((period) => (
            <button
              key={period.value}
              onClick={() => setTimePeriod(period.value as any)}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: 500,
                backgroundColor: timePeriod === period.value ? '#0f172a' : '#f1f5f9',
                color: timePeriod === period.value ? 'white' : '#475569',
                transition: 'all 0.2s',
              }}
            >
              {period.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Metrics */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '20px',
        marginBottom: '32px',
      }}>
        {[
          { label: 'Total Pedidos', value: metrics.total, color: '#3b82f6', prefix: '' },
          { label: 'Receita', value: metrics.revenue.toFixed(2), color: '#10b981', prefix: '€' },
          { label: 'Lucro', value: metrics.profit.toFixed(2), color: '#8b5cf6', prefix: '€' },
          { label: 'Taxa de Conversao', value: metrics.conversionRate.toFixed(1), color: '#f59e0b', prefix: '', suffix: '%' },
        ].map((metric, i) => (
          <div key={i} style={{
            backgroundColor: '#ffffff',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            border: '1px solid #e2e8f0',
          }}>
            <p style={{
              margin: '0 0 12px',
              fontSize: '13px',
              color: '#64748b',
              fontWeight: 500,
              textTransform: 'uppercase',
            }}>
              {metric.label}
            </p>
            <p style={{
              margin: 0,
              fontSize: '32px',
              fontWeight: 700,
              color: metric.color,
            }}>
              {metric.prefix}{metric.value}{metric.suffix || ''}
            </p>
          </div>
        ))}
      </div>

      {/* Two Column Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Status Breakdown */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          border: '1px solid #e2e8f0',
        }}>
          <h2 style={{ margin: '0 0 20px', fontSize: '16px', fontWeight: 600, color: '#0f172a' }}>
            Pedidos por Estado
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[
              { label: 'Por Tratar', value: metrics.byStatus.pending_selection, color: '#3b82f6' },
              { label: 'Propostas Enviadas', value: metrics.byStatus.proposal_sent, color: '#8b5cf6' },
              { label: 'Pronto para Confirmar', value: metrics.byStatus.accepted, color: '#f59e0b' },
              { label: 'Confirmado', value: metrics.byStatus.invoiced, color: '#10b981' },
              { label: 'Nao Confirmado', value: metrics.byStatus.cancelled, color: '#ef4444' },
            ].map((status, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                  width: '12px',
                  height: '12px',
                  borderRadius: '4px',
                  backgroundColor: status.color,
                }} />
                <span style={{ flex: 1, fontSize: '14px', color: '#475569' }}>
                  {status.label}
                </span>
                <span style={{ fontSize: '14px', fontWeight: 600, color: '#0f172a' }}>
                  {status.value}
                </span>
                {metrics.total > 0 && (
                  <span style={{ fontSize: '12px', color: '#94a3b8', width: '45px', textAlign: 'right' }}>
                    {(status.value / metrics.total * 100).toFixed(0)}%
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Financial Summary */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          border: '1px solid #e2e8f0',
        }}>
          <h2 style={{ margin: '0 0 20px', fontSize: '16px', fontWeight: 600, color: '#0f172a' }}>
            Resumo Financeiro
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              padding: '12px 16px',
              backgroundColor: '#f8fafc',
              borderRadius: '8px',
            }}>
              <span style={{ fontSize: '14px', color: '#64748b' }}>Receita Total</span>
              <span style={{ fontSize: '14px', fontWeight: 600, color: '#10b981' }}>€{metrics.revenue.toFixed(2)}</span>
            </div>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              padding: '12px 16px',
              backgroundColor: '#f8fafc',
              borderRadius: '8px',
            }}>
              <span style={{ fontSize: '14px', color: '#64748b' }}>Custo Total</span>
              <span style={{ fontSize: '14px', fontWeight: 600, color: '#ef4444' }}>€{metrics.cost.toFixed(2)}</span>
            </div>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              padding: '12px 16px',
              backgroundColor: '#ecfdf5',
              borderRadius: '8px',
              border: '1px solid #a7f3d0',
            }}>
              <span style={{ fontSize: '14px', fontWeight: 500, color: '#047857' }}>Lucro Total</span>
              <span style={{ fontSize: '14px', fontWeight: 700, color: '#047857' }}>€{metrics.profit.toFixed(2)}</span>
            </div>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              padding: '12px 16px',
              backgroundColor: '#f5f3ff',
              borderRadius: '8px',
              border: '1px solid #ddd6fe',
            }}>
              <span style={{ fontSize: '14px', fontWeight: 500, color: '#6d28d9' }}>Margem Media</span>
              <span style={{ fontSize: '14px', fontWeight: 700, color: '#6d28d9' }}>{avgMargin.toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Completed */}
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        border: '1px solid #e2e8f0',
        marginTop: '24px',
      }}>
        <h2 style={{ margin: '0 0 20px', fontSize: '16px', fontWeight: 600, color: '#0f172a' }}>
          Ultimos Confirmados
        </h2>
        {filteredRequests.filter(r => r.status === 'invoiced').length === 0 ? (
          <p style={{ color: '#94a3b8', fontSize: '14px', margin: 0 }}>
            Nenhum pedido confirmado neste periodo
          </p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {filteredRequests
              .filter(r => r.status === 'invoiced')
              .slice(0, 5)
              .map((req) => (
                <div key={req.id} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px 16px',
                  backgroundColor: '#f8fafc',
                  borderRadius: '8px',
                }}>
                  <div>
                    <span style={{ fontSize: '14px', fontWeight: 500, color: '#0f172a' }}>
                      {req.client_name || req.client_email}
                    </span>
                    <span style={{ fontSize: '12px', color: '#94a3b8', marginLeft: '12px' }}>
                      {req.selected_partner_name}
                    </span>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <span style={{ fontSize: '14px', fontWeight: 600, color: '#10b981' }}>
                      €{req.price?.toFixed(2)}
                    </span>
                    {req.cost_price && req.price && (
                      <span style={{ fontSize: '12px', color: '#8b5cf6', marginLeft: '8px' }}>
                        (+€{(req.price - req.cost_price).toFixed(2)})
                      </span>
                    )}
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
