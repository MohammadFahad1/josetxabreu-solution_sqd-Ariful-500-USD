'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { toast } from 'sonner';
import {
  RentalRequest,
  Partner,
  Vehicle,
  getRequest,
  getAllCategories,
  getPartnersByCategory,
  getPartnerVehicles,
  getPartner,
  selectPartner,
  sendProposal,
  sendPartnerRequest,
  markAccepted,
  confirmBooking,
  updatePartnerNotes,
  formatStatus,
} from '@/lib/api';
import ConfirmDialog from '@/components/ConfirmDialog';

export default function RequestDetail() {
  const params = useParams();
  const router = useRouter();
  const requestId = params.id as string;

  const [request, setRequest] = useState<RentalRequest | null>(null);
  const [allCategories, setAllCategories] = useState<string[]>([]);
  const [partners, setPartners] = useState<Partner[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);

  // New flow: Category → Partner → Vehicle → Price
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedPartnerId, setSelectedPartnerId] = useState<string | "">("");
  const [selectedVehicleId, setSelectedVehicleId] = useState<string | null>(null);
  const [costPrice, setCostPrice] = useState('');
  const [price, setPrice] = useState('');
  const [partnerNotes, setPartnerNotes] = useState('');
  const [notesSaving, setNotesSaving] = useState(false);
  const [notesPartnerId, setNotesPartnerId] = useState<string | "">("");

  const [loading, setLoading] = useState(true);
  const [partnersLoading, setPartnersLoading] = useState(false);
  const [vehiclesLoading, setVehiclesLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Dialog states
  const [dialogState, setDialogState] = useState<{
    isOpen: boolean;
    type: 'proposal' | 'accepted' | 'confirm' | 'partner_request' | null;
  }>({ isOpen: false, type: null });

  // Initial load - Load request and all categories
  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [requestData, categoriesData] = await Promise.all([
          getRequest(requestId),
          getAllCategories(),
        ]);
        setRequest(requestData);
        setAllCategories(categoriesData);

        // Restore previous prices if exists
        if (requestData.cost_price) {
          setCostPrice(requestData.cost_price.toString());
        }
        if (requestData.price) {
          setPrice(requestData.price.toString());
        }
        // Load partner notes if a partner is already selected
        if (requestData.selected_partner_id) {
          try {
            const partnerData = await getPartner(requestData.selected_partner_id);
            setPartnerNotes(partnerData.notes || '');
            setNotesPartnerId(requestData.selected_partner_id);
          } catch (e) {
            console.error('Failed to load partner notes:', e);
          }
        }
      } catch (e) {
        setError('Erro ao carregar pedido');
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [requestId]);

  // Load partners when category changes (NEW FLOW: Category first)
  useEffect(() => {
    if (!selectedCategory) {
      setPartners([]);
      setSelectedPartnerId("");
      setVehicles([]);
      setSelectedVehicleId(null);
      return;
    }

    const loadPartners = async () => {
      try {
        setPartnersLoading(true);
        const pts = await getPartnersByCategory(selectedCategory);
        setPartners(pts);
        setSelectedPartnerId("");
        setVehicles([]);
        setSelectedVehicleId(null);
      } catch (e) {
        console.error('Failed to load partners:', e);
        toast.error('Erro ao carregar parceiros');
      } finally {
        setPartnersLoading(false);
      }
    };
    loadPartners();
  }, [selectedCategory]);

  // Load vehicles and partner notes when partner changes (within selected category)
  useEffect(() => {
    if (!selectedPartnerId || !selectedCategory) {
      setVehicles([]);
      setSelectedVehicleId(null);
      return;
    }

    const loadVehiclesAndNotes = async () => {
      try {
        setVehiclesLoading(true);
        const [vehs, partnerData] = await Promise.all([
          getPartnerVehicles(selectedPartnerId, selectedCategory),
          getPartner(selectedPartnerId),
        ]);
        setVehicles(vehs);
        setSelectedVehicleId(null);
        // Load partner notes
        setPartnerNotes(partnerData.notes || '');
        setNotesPartnerId(selectedPartnerId);
      } catch (e) {
        console.error('Failed to load vehicles:', e);
        toast.error('Erro ao carregar veículos');
      } finally {
        setVehiclesLoading(false);
      }
    };
    loadVehiclesAndNotes();
  }, [selectedPartnerId, selectedCategory]);

  const handleSelectPartner = async () => {
    if (!selectedPartnerId || !selectedVehicleId || !costPrice || !price) {
      toast.error('Por favor selecione um parceiro, veículo e introduza os preços');
      return;
    }

    try {
      setActionLoading(true);
      await selectPartner(requestId, selectedPartnerId, selectedVehicleId, parseFloat(costPrice), parseFloat(price));
      const updated = await getRequest(requestId);
      setRequest(updated);
      toast.success('Parceiro e veículo selecionados com sucesso');
    } catch (e) {
      toast.error('Erro ao selecionar parceiro');
      console.error(e);
    } finally {
      setActionLoading(false);
    }
  };

  const handleSendProposal = async () => {
    try {
      setActionLoading(true);
      setDialogState({ isOpen: false, type: null });
      await sendProposal(requestId);
      const updated = await getRequest(requestId);
      setRequest(updated);
      toast.success('Proposta enviada com sucesso');
    } catch (e) {
      toast.error('Erro ao enviar proposta');
      console.error(e);
    } finally {
      setActionLoading(false);
    }
  };

  const handleMarkAccepted = async () => {
    try {
      setActionLoading(true);
      setDialogState({ isOpen: false, type: null });
      await markAccepted(requestId);
      const updated = await getRequest(requestId);
      setRequest(updated);
      toast.success('Pedido marcado como aceite');
    } catch (e) {
      toast.error('Erro ao marcar como aceite');
      console.error(e);
    } finally {
      setActionLoading(false);
    }
  };

  const handleConfirmBooking = async () => {
    try {
      setActionLoading(true);
      setDialogState({ isOpen: false, type: null });
      await confirmBooking(requestId);
      const updated = await getRequest(requestId);
      setRequest(updated);
      toast.success('Reserva confirmada com sucesso');
    } catch (e) {
      toast.error('Erro ao confirmar reserva');
      console.error(e);
    } finally {
      setActionLoading(false);
    }
  };

  const handleSendPartnerRequest = async () => {
    try {
      setActionLoading(true);
      setDialogState({ isOpen: false, type: null });
      const result = await sendPartnerRequest(requestId);
      toast.success(result.message);
    } catch (e: any) {
      toast.error(e.message || 'Erro ao enviar pedido ao parceiro');
      console.error(e);
    } finally {
      setActionLoading(false);
    }
  };

  const handleSavePartnerNotes = async () => {
    if (!notesPartnerId) {
      toast.error('Selecione um parceiro primeiro');
      return;
    }
    try {
      setNotesSaving(true);
      await updatePartnerNotes(notesPartnerId, partnerNotes);
      toast.success('Notas do parceiro guardadas');
    } catch (e) {
      toast.error('Erro ao guardar notas do parceiro');
      console.error(e);
    } finally {
      setNotesSaving(false);
    }
  };

  // Get price suggestion based on selected vehicle and rental duration
  const getSuggestedPrice = () => {
    if (!selectedVehicleId || !request?.pickup_date || !request?.return_date) return null;

    const vehicle = vehicles.find(v => v.id === selectedVehicleId);
    if (!vehicle) return null;

    const start = new Date(request.pickup_date);
    const end = new Date(request.return_date);
    const days = Math.max(1, Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)));

    // Determine which price tier to use (this is the COST price from partner)
    let dailyRate = vehicle.price_1_3_days;
    if (days >= 30 && vehicle.price_monthly) {
      // Use monthly rate
      return { costTotal: vehicle.price_monthly, days, rate: vehicle.price_monthly, type: 'monthly' };
    } else if (days >= 7 && vehicle.price_7_29_days) {
      dailyRate = vehicle.price_7_29_days;
    } else if (days >= 4 && vehicle.price_4_6_days) {
      dailyRate = vehicle.price_4_6_days;
    }

    if (!dailyRate) return null;
    return { costTotal: dailyRate * days, days, rate: dailyRate, type: 'daily' };
  };

  const applySuggestedPrice = () => {
    const suggestion = getSuggestedPrice();
    if (suggestion) {
      setCostPrice(suggestion.costTotal.toFixed(2));
      // Suggest client price with 20% markup
      setPrice((suggestion.costTotal * 1.2).toFixed(2));
    }
  };

  const statusColorMap: Record<string, { bg: string; text: string; border: string }> = {
    pending_info: { bg: '#fef3c7', text: '#92400e', border: '#fcd34d' },
    pending_selection: { bg: '#cffafe', text: '#0e7490', border: '#22d3ee' },
    proposal_sent: { bg: '#f3e8ff', text: '#7c3aed', border: '#c4b5fd' },
    accepted: { bg: '#d1fae5', text: '#047857', border: '#34d399' },
    invoiced: { bg: '#dbeafe', text: '#1d4ed8', border: '#60a5fa' },
    cancelled: { bg: '#fee2e2', text: '#dc2626', border: '#f87171' },
  };

  const getDialogConfig = () => {
    switch (dialogState.type) {
      case 'proposal':
        return {
          title: 'Enviar Proposta',
          message: `Tem a certeza que deseja enviar a proposta ao cliente ${request?.client_name || request?.client_email}?`,
          confirmText: 'Enviar',
          onConfirm: handleSendProposal,
        };
      case 'accepted':
        return {
          title: 'Marcar como Aceite',
          message: 'Tem a certeza que deseja marcar este pedido como aceite?',
          confirmText: 'Confirmar',
          onConfirm: handleMarkAccepted,
        };
      case 'confirm':
        return {
          title: 'Confirmar Reserva',
          message: 'Tem a certeza que deseja confirmar esta reserva? Um email de confirmação será enviado ao cliente.',
          confirmText: 'Confirmar Reserva',
          onConfirm: handleConfirmBooking,
        };
      case 'partner_request':
        return {
          title: 'Enviar Pedido ao Parceiro',
          message: `Tem a certeza que deseja enviar o pedido de confirmação ao parceiro ${request?.selected_partner_name}?`,
          confirmText: 'Enviar Pedido',
          onConfirm: handleSendPartnerRequest,
        };
      default:
        return {
          title: '',
          message: '',
          confirmText: 'Confirmar',
          onConfirm: () => {},
        };
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '80px', color: '#64748b', fontSize: '14px' }}>
        A carregar...
      </div>
    );
  }

  if (error || !request) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '80px',
        color: '#dc2626',
        fontSize: '14px',
      }}>
        {error || 'Pedido nao encontrado'}
      </div>
    );
  }

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('pt-PT', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  };

  const statusStyle = statusColorMap[request.status] || { bg: '#f1f5f9', text: '#475569', border: '#cbd5e1' };
  const dialogConfig = getDialogConfig();
  const priceSuggestion = getSuggestedPrice();

  return (
    <div>
      {/* Confirm Dialog */}
      <ConfirmDialog
        isOpen={dialogState.isOpen}
        title={dialogConfig.title}
        message={dialogConfig.message}
        confirmText={dialogConfig.confirmText}
        cancelText="Cancelar"
        onConfirm={dialogConfig.onConfirm}
        onCancel={() => setDialogState({ isOpen: false, type: null })}
      />

      {/* Back Button */}
      <button
        onClick={() => router.push('/')}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '10px 16px',
          border: '1px solid #e2e8f0',
          borderRadius: '8px',
          cursor: 'pointer',
          fontSize: '13px',
          fontWeight: 500,
          backgroundColor: '#ffffff',
          color: '#475569',
          marginBottom: '24px',
          transition: 'all 0.2s',
        }}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        Voltar ao Painel
      </button>

      {/* Header */}
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        padding: '28px',
        marginBottom: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        border: '1px solid #e2e8f0',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h1 style={{ margin: '0 0 8px', fontSize: '24px', fontWeight: 700, color: '#0f172a' }}>
              {request.client_name || 'Cliente Desconhecido'}
            </h1>
            <p style={{ margin: 0, color: '#64748b', fontSize: '14px' }}>{request.client_email}</p>
            {request.client_phone && (
              <p style={{ margin: '4px 0 0', color: '#64748b', fontSize: '14px' }}>{request.client_phone}</p>
            )}
            {request.client_vat && (
              <p style={{ margin: '4px 0 0', color: '#64748b', fontSize: '14px' }}>NIF: {request.client_vat}</p>
            )}
          </div>
          <span style={{
            backgroundColor: statusStyle.bg,
            color: statusStyle.text,
            padding: '8px 16px',
            borderRadius: '20px',
            fontSize: '13px',
            fontWeight: 600,
            border: `1px solid ${statusStyle.border}`,
          }}>
            {formatStatus(request.status)}
          </span>
        </div>
      </div>

      {/* Rental Details */}
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        padding: '28px',
        marginBottom: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        border: '1px solid #e2e8f0',
      }}>
        <h2 style={{ margin: '0 0 24px', fontSize: '18px', fontWeight: 600, color: '#0f172a' }}>
          Detalhes do Aluguer
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Data de Levantamento
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {formatDate(request.pickup_date)}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Data de Devolução
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {formatDate(request.return_date)}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Local de Levantamento
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {request.pickup_location || 'Não especificado'}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Local de Devolução
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {request.return_location || request.pickup_location || 'Não especificado'}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Tipo de Veículo
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {request.vehicle_type?.replace(/_/g, ' ') || 'Não especificado'}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Pedidos Especiais
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', color: '#1e293b' }}>
              {request.special_requests || 'Nenhum'}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Nome do Condutor
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {request.driver_name || 'Não especificado'}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Artista / Projeto / Evento
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {request.artist_project_event || 'Não especificado'}
            </p>
          </div>
          <div>
            <label style={{
              fontSize: '11px',
              color: '#94a3b8',
              textTransform: 'uppercase',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}>
              Cidades de Destino
            </label>
            <p style={{ margin: '8px 0 0', fontSize: '15px', fontWeight: 500, color: '#1e293b' }}>
              {request.destination_cities || 'Não especificado'}
            </p>
          </div>
        </div>
      </div>

      {/* Partner & Vehicle Selection */}
      {(request.status === 'pending_selection' || request.status === 'proposal_sent') && (
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          padding: '28px',
          marginBottom: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          border: '2px solid #0891b2',
        }}>
          <h2 style={{ margin: '0 0 24px', fontSize: '18px', fontWeight: 600, color: '#0891b2' }}>
            Selecionar Parceiro e Veículo
          </h2>

          {/* Step 1: Category Selection (NEW FLOW) */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '13px',
              fontWeight: 600,
              color: '#475569',
            }}>
              1. Categoria
            </label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {allCategories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    border: selectedCategory === cat ? '2px solid #0891b2' : '1px solid #e2e8f0',
                    backgroundColor: selectedCategory === cat ? '#ecfeff' : '#ffffff',
                    color: selectedCategory === cat ? '#0891b2' : '#475569',
                    cursor: 'pointer',
                    fontSize: '13px',
                    fontWeight: 500,
                    transition: 'all 0.2s',
                  }}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          {/* Step 2: Partner Selection (sorted by cheapest price in this category) */}
          {selectedCategory && (
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '13px',
                fontWeight: 600,
                color: '#475569',
              }}>
                2. Parceiro <span style={{ fontWeight: 400, color: '#94a3b8' }}>(ordenado por preço mais baixo)</span>
              </label>
              {partnersLoading ? (
                <p style={{ color: '#64748b', fontSize: '14px' }}>A carregar parceiros...</p>
              ) : partners.length === 0 ? (
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>Nenhum parceiro disponível nesta categoria</p>
              ) : (
                <select
                  value={selectedPartnerId || ''}
                  onChange={(e) => setSelectedPartnerId(e.target.value ? e.target.value : "")}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                    fontSize: '14px',
                    backgroundColor: '#ffffff',
                    color: '#1e293b',
                  }}
                >
                  <option value="">Selecionar parceiro...</option>
                  {partners.map((partner, index) => (
                    <option key={partner.id} value={partner.id}>
                      {index === 0 ? '⭐ ' : ''}{partner.name}{index === 0 ? ' (mais barato)' : ''}
                    </option>
                  ))}
                </select>
              )}
            </div>
          )}

          {/* Step 3: Vehicle Selection */}
          {selectedPartnerId && (
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '13px',
                fontWeight: 600,
                color: '#475569',
              }}>
                3. Veículo
              </label>
              {vehiclesLoading ? (
                <p style={{ color: '#64748b', fontSize: '14px' }}>A carregar veículos...</p>
              ) : vehicles.length === 0 ? (
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>Nenhum veículo disponível nesta categoria</p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {vehicles.map((vehicle) => (
                    <div
                      key={vehicle.id}
                      onClick={() => setSelectedVehicleId(vehicle.id)}
                      style={{
                        padding: '16px',
                        borderRadius: '8px',
                        border: selectedVehicleId === vehicle.id ? '2px solid #0891b2' : '1px solid #e2e8f0',
                        backgroundColor: selectedVehicleId === vehicle.id ? '#ecfeff' : '#ffffff',
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <div>
                          <span style={{
                            fontSize: '12px',
                            fontWeight: 600,
                            color: '#0891b2',
                            backgroundColor: '#ecfeff',
                            padding: '2px 8px',
                            borderRadius: '4px',
                            marginRight: '8px',
                          }}>
                            {vehicle.group_code}
                          </span>
                          <span style={{ fontSize: '14px', fontWeight: 500, color: '#1e293b' }}>
                            {vehicle.description}
                          </span>
                        </div>
                      </div>
                      <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(4, 1fr)',
                        gap: '12px',
                        marginTop: '12px',
                        fontSize: '12px',
                      }}>
                        <div>
                          <span style={{ color: '#94a3b8' }}>1-3 dias:</span>
                          <span style={{ color: '#1e293b', fontWeight: 500, marginLeft: '4px' }}>
                            {vehicle.price_1_3_days ? `€${vehicle.price_1_3_days.toFixed(2)}` : '-'}
                          </span>
                        </div>
                        <div>
                          <span style={{ color: '#94a3b8' }}>4-6 dias:</span>
                          <span style={{ color: '#1e293b', fontWeight: 500, marginLeft: '4px' }}>
                            {vehicle.price_4_6_days ? `€${vehicle.price_4_6_days.toFixed(2)}` : '-'}
                          </span>
                        </div>
                        <div>
                          <span style={{ color: '#94a3b8' }}>7-29 dias:</span>
                          <span style={{ color: '#1e293b', fontWeight: 500, marginLeft: '4px' }}>
                            {vehicle.price_7_29_days ? `€${vehicle.price_7_29_days.toFixed(2)}` : '-'}
                          </span>
                        </div>
                        <div>
                          <span style={{ color: '#94a3b8' }}>Mensal:</span>
                          <span style={{ color: '#1e293b', fontWeight: 500, marginLeft: '4px' }}>
                            {vehicle.price_monthly ? `€${vehicle.price_monthly.toFixed(2)}` : '-'}
                          </span>
                        </div>
                      </div>
                      {(vehicle.franchise || vehicle.min_age || vehicle.notes) && (
                        <div style={{
                          marginTop: '8px',
                          paddingTop: '8px',
                          borderTop: '1px solid #e2e8f0',
                          fontSize: '11px',
                          color: '#64748b',
                        }}>
                          {vehicle.franchise !== null && vehicle.franchise > 0 && (
                            <span style={{ marginRight: '12px' }}>Franquia: €{vehicle.franchise.toFixed(2)}</span>
                          )}
                          {vehicle.min_age && (
                            <span style={{ marginRight: '12px' }}>Idade min: {vehicle.min_age}</span>
                          )}
                          {vehicle.license_years && (
                            <span style={{ marginRight: '12px' }}>Carta: {vehicle.license_years}+ anos</span>
                          )}
                          {vehicle.notes && (
                            <span>{vehicle.notes}</span>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Step 4: Prices */}
          {selectedVehicleId && (
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '13px',
                fontWeight: 600,
                color: '#475569',
              }}>
                4. Preços
              </label>

              {/* Suggest button */}
              {priceSuggestion && (
                <button
                  onClick={applySuggestedPrice}
                  style={{
                    padding: '10px 16px',
                    borderRadius: '8px',
                    border: '1px solid #10b981',
                    backgroundColor: '#ecfdf5',
                    cursor: 'pointer',
                    fontSize: '13px',
                    color: '#047857',
                    marginBottom: '16px',
                    fontWeight: 500,
                  }}
                >
                  Calcular preços: {priceSuggestion.days} dias @ €{priceSuggestion.rate.toFixed(2)}{priceSuggestion.type === 'monthly' ? '/mês' : '/dia'}
                </button>
              )}

              <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
                {/* Cost Price */}
                <div>
                  <label style={{
                    display: 'block',
                    marginBottom: '6px',
                    fontSize: '12px',
                    color: '#64748b',
                  }}>
                    Preço de Custo (Parceiro)
                  </label>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <input
                      type="number"
                      value={costPrice}
                      onChange={(e) => setCostPrice(e.target.value)}
                      placeholder="0.00"
                      step="0.01"
                      style={{
                        width: '130px',
                        padding: '12px 16px',
                        borderRadius: '8px',
                        border: '1px solid #e2e8f0',
                        fontSize: '14px',
                        backgroundColor: '#fef3c7',
                      }}
                    />
                    <span style={{ color: '#64748b', fontSize: '14px' }}>€</span>
                  </div>
                </div>

                {/* Client Price */}
                <div>
                  <label style={{
                    display: 'block',
                    marginBottom: '6px',
                    fontSize: '12px',
                    color: '#64748b',
                  }}>
                    Preço Cliente (Final)
                  </label>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <input
                      type="number"
                      value={price}
                      onChange={(e) => setPrice(e.target.value)}
                      placeholder="0.00"
                      step="0.01"
                      style={{
                        width: '130px',
                        padding: '12px 16px',
                        borderRadius: '8px',
                        border: '1px solid #10b981',
                        fontSize: '14px',
                        backgroundColor: '#ecfdf5',
                      }}
                    />
                    <span style={{ color: '#64748b', fontSize: '14px' }}>€</span>
                  </div>
                </div>

                {/* Margin indicator */}
                {costPrice && price && parseFloat(costPrice) > 0 && (
                  <div style={{ display: 'flex', alignItems: 'flex-end', paddingBottom: '8px' }}>
                    <span style={{
                      fontSize: '13px',
                      color: parseFloat(price) > parseFloat(costPrice) ? '#047857' : '#dc2626',
                      fontWeight: 500,
                    }}>
                      Margem: €{(parseFloat(price) - parseFloat(costPrice)).toFixed(2)} ({(((parseFloat(price) - parseFloat(costPrice)) / parseFloat(costPrice)) * 100).toFixed(0)}%)
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Save Button */}
          <button
            onClick={handleSelectPartner}
            disabled={actionLoading || !selectedPartnerId || !selectedVehicleId || !costPrice || !price}
            style={{
              padding: '12px 24px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: (!selectedPartnerId || !selectedVehicleId || !costPrice || !price) ? '#94a3b8' : '#0891b2',
              color: 'white',
              cursor: (!selectedPartnerId || !selectedVehicleId || !costPrice || !price) ? 'not-allowed' : 'pointer',
              fontSize: '14px',
              fontWeight: 600,
              opacity: actionLoading ? 0.7 : 1,
              transition: 'all 0.2s',
            }}
          >
            {actionLoading ? 'A guardar...' : 'Guardar Seleção'}
          </button>

          {/* Current Selection Display */}
          {request.selected_partner_name && request.selected_vehicle_description && (
            <div style={{
              marginTop: '20px',
              padding: '16px 20px',
              backgroundColor: '#ecfdf5',
              borderRadius: '8px',
              border: '1px solid #a7f3d0',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#047857" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
                <span style={{ fontSize: '14px', color: '#047857', fontWeight: 500 }}>
                  Seleção atual: {request.selected_partner_name} - {request.selected_vehicle_description}
                </span>
              </div>
              <div style={{ display: 'flex', gap: '24px', marginLeft: '32px', fontSize: '13px' }}>
                <span style={{ color: '#92400e', backgroundColor: '#fef3c7', padding: '4px 8px', borderRadius: '4px' }}>
                  Custo: €{request.cost_price?.toFixed(2) || '—'}
                </span>
                <span style={{ color: '#047857', backgroundColor: '#d1fae5', padding: '4px 8px', borderRadius: '4px' }}>
                  Cliente: €{request.price?.toFixed(2) || '—'}
                </span>
                {request.cost_price && request.price && (
                  <span style={{ color: '#6b7280' }}>
                    Margem: €{(request.price - request.cost_price).toFixed(2)}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        padding: '28px',
        marginBottom: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
        border: '1px solid #e2e8f0',
      }}>
        <h2 style={{ margin: '0 0 20px', fontSize: '18px', fontWeight: 600, color: '#0f172a' }}>
          Ações
        </h2>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          {request.status === 'pending_selection' && request.selected_partner_id && (
            <>
              <button
                onClick={() => setDialogState({ isOpen: true, type: 'partner_request' })}
                disabled={actionLoading}
                style={{
                  padding: '12px 24px',
                  borderRadius: '8px',
                  border: '2px solid #f59e0b',
                  backgroundColor: '#fffbeb',
                  color: '#b45309',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: 600,
                  transition: 'all 0.2s',
                }}
              >
                Enviar Pedido ao Parceiro
              </button>
              <button
                onClick={() => setDialogState({ isOpen: true, type: 'proposal' })}
                disabled={actionLoading}
                style={{
                  padding: '12px 24px',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: 600,
                  transition: 'all 0.2s',
                }}
              >
                Enviar Proposta ao Cliente
              </button>
            </>
          )}

          {request.status === 'proposal_sent' && (
            <button
              onClick={() => setDialogState({ isOpen: true, type: 'accepted' })}
              disabled={actionLoading}
              style={{
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: '#10b981',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 600,
                transition: 'all 0.2s',
              }}
            >
              Marcar como Aceite
            </button>
          )}

          {request.status === 'accepted' && (
            <button
              onClick={() => setDialogState({ isOpen: true, type: 'confirm' })}
              disabled={actionLoading}
              style={{
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: '#10b981',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 600,
                transition: 'all 0.2s',
              }}
            >
              Confirmar Reserva
            </button>
          )}

          {!request.selected_partner_id && request.status === 'pending_selection' && (
            <p style={{ color: '#94a3b8', fontSize: '14px', margin: 0 }}>
              Selecione um parceiro e veículo acima para ver as ações disponíveis
            </p>
          )}
        </div>
      </div>

      {/* Partner Notes - Only show when a partner is selected */}
      {(notesPartnerId || request.selected_partner_id) && (
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          padding: '28px',
          marginBottom: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          border: '1px solid #e2e8f0',
        }}>
          <h2 style={{ margin: '0 0 16px', fontSize: '18px', fontWeight: 600, color: '#0f172a' }}>
            Notas do Parceiro: {
              partners.find(p => p.id === (notesPartnerId || request.selected_partner_id))?.name ||
              request.selected_partner_name ||
              'Parceiro'
            }
          </h2>
          <p style={{ margin: '0 0 12px', fontSize: '13px', color: '#64748b' }}>
            Estas notas são guardadas no parceiro e aparecem em todos os pedidos com este parceiro.
          </p>
          <textarea
            value={partnerNotes}
            onChange={(e) => setPartnerNotes(e.target.value)}
            placeholder="Adicionar notas sobre este parceiro..."
            style={{
              width: '100%',
              minHeight: '120px',
              padding: '16px',
              borderRadius: '8px',
              border: '1px solid #e2e8f0',
              fontSize: '14px',
              fontFamily: 'inherit',
              resize: 'vertical',
              backgroundColor: '#f8fafc',
            }}
          />
          <button
            onClick={handleSavePartnerNotes}
            disabled={notesSaving || !notesPartnerId}
            style={{
              marginTop: '12px',
              padding: '10px 20px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: (!notesPartnerId) ? '#94a3b8' : '#0f172a',
              color: 'white',
              cursor: (notesSaving || !notesPartnerId) ? 'not-allowed' : 'pointer',
              fontSize: '13px',
              fontWeight: 600,
              opacity: notesSaving ? 0.7 : 1,
            }}
          >
            {notesSaving ? 'A guardar...' : 'Guardar Notas do Parceiro'}
          </button>
        </div>
      )}

      {/* Original Email */}
      {request.original_email_subject && (
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          padding: '28px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          border: '1px solid #e2e8f0',
        }}>
          <h2 style={{ margin: '0 0 16px', fontSize: '18px', fontWeight: 600, color: '#0f172a' }}>
            Email Original
          </h2>
          <div style={{
            backgroundColor: '#f8fafc',
            padding: '20px',
            borderRadius: '8px',
            border: '1px solid #e2e8f0',
            fontFamily: 'monospace',
            fontSize: '13px',
            color: '#475569',
            whiteSpace: 'pre-wrap',
            maxHeight: '300px',
            overflow: 'auto',
          }}>
            <strong style={{ color: '#1e293b' }}>Assunto:</strong> {request.original_email_subject}
          </div>
        </div>
      )}
    </div>
  );
}
