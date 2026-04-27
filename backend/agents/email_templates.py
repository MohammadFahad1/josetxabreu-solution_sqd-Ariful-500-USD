"""Professional HTML email templates for IRWT."""

from datetime import date
from typing import Optional

LOGO_URL = "https://res.cloudinary.com/dsntusqam/image/upload/v1765271950/logo_eaj0du.png"

# Base HTML template with professional styling
BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; line-height: 1.6;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8fafc;">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); overflow: hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #ffffff; padding: 32px 40px; text-align: center; border-bottom: 1px solid #e2e8f0;">
                            <img src="{logo_url}" alt="IRWT" style="height: 50px; width: auto;" />
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            {content}
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 24px 40px; border-top: 1px solid #e2e8f0;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td style="text-align: center;">
                                        <p style="margin: 0 0 8px; font-size: 14px; color: #64748b; font-weight: 600;">IRWT - Aluguer de Carrinhas</p>
                                        <p style="margin: 0; font-size: 12px; color: #94a3b8;">Este email foi enviado automaticamente. Por favor responda diretamente a este email para qualquer questão.</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def _format_portuguese_date(d: date) -> str:
    """Format date in Portuguese."""
    weekdays = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo",
    }
    months = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
    }
    weekday = weekdays[d.weekday()]
    month = months[d.month]
    return f"{weekday}, {d.day} de {month} de {d.year}"


def _get_vehicle_display(vehicle_type: str) -> str:
    """Get display name for vehicle type."""
    return {
        "small_van": "Carrinha pequena",
        "medium_van": "Carrinha média",
        "large_van": "Carrinha grande",
        "9_seater": "Carrinha de 9 lugares",
        "12_seater": "Carrinha de 12 lugares",
        "minibus": "Minibus",
        "cargo_van": "Carrinha de carga",
    }.get(vehicle_type, vehicle_type)


def generate_proposal_html(
    client_name: str,
    pickup_date: date,
    return_date: date,
    pickup_location: str,
    return_location: str,
    vehicle_type: str,
    partner_name: str,
    price: float,
) -> str:
    """Generate professional HTML proposal email."""

    num_days = (return_date - pickup_date).days
    if num_days < 1:
        num_days = 1

    vehicle_display = _get_vehicle_display(vehicle_type)
    pickup_date_str = _format_portuguese_date(pickup_date)
    return_date_str = _format_portuguese_date(return_date)

    content = f"""
        <!-- Greeting -->
        <h1 style="margin: 0 0 24px; font-size: 24px; font-weight: 700; color: #0f172a;">
            Olá {client_name},
        </h1>

        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Obrigado pelo seu pedido de aluguer. Temos o prazer de apresentar a seguinte proposta:
        </p>

        <!-- Rental Details Card -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8fafc; border-radius: 12px; margin-bottom: 24px;">
            <tr>
                <td style="padding: 24px;">
                    <h2 style="margin: 0 0 20px; font-size: 16px; font-weight: 600; color: #0891b2; text-transform: uppercase; letter-spacing: 0.05em;">
                        Detalhes do Aluguer
                    </h2>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Tipo de Veiculo</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{vehicle_display}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Data de Levantamento</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{pickup_date_str}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Local de Levantamento</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{pickup_location}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Data de Devolucao</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{return_date_str}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Local de Devolucao</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{return_location}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Duração</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{num_days} dia(s)</span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Price Card -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 12px; margin-bottom: 24px;">
            <tr>
                <td style="padding: 24px; text-align: center;">
                    <span style="font-size: 14px; color: rgba(255,255,255,0.9); display: block; margin-bottom: 8px;">Preço Total</span>
                    <span style="font-size: 36px; font-weight: 700; color: #ffffff;">{price:.2f} EUR</span>
                </td>
            </tr>
        </table>

        <!-- Terms -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #fef3c7; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #f59e0b;">
            <tr>
                <td style="padding: 20px 24px;">
                    <h3 style="margin: 0 0 12px; font-size: 14px; font-weight: 600; color: #92400e;">Termos e Condições</h3>
                    <ul style="margin: 0; padding-left: 20px; color: #92400e; font-size: 13px;">
                        <li style="margin-bottom: 6px;">Pagamento integral necessário no momento da confirmação</li>
                        <li style="margin-bottom: 6px;">Carta de condução válida obrigatória no levantamento</li>
                        <li style="margin-bottom: 6px;">Política de combustivel: Cheio para Cheio</li>
                        <li style="margin-bottom: 6px;">Cancelamento: Gratuito até 48 horas antes do levantamento</li>
                        <li style="margin-bottom: 0;">Poderá ser exigida caução no momento do levantamento</li>
                    </ul>
                </td>
            </tr>
        </table>

        <!-- CTA -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom: 24px;">
            <tr>
                <td style="text-align: center; padding: 20px; background-color: #eff6ff; border-radius: 12px; border: 2px dashed #3b82f6;">
                    <p style="margin: 0 0 8px; font-size: 15px; color: #1e40af; font-weight: 600;">
                        Para confirmar esta reserva
                    </p>
                    <p style="margin: 0; font-size: 14px; color: #3b82f6;">
                        Basta responder a este email com <strong>"Aceito"</strong> ou <strong>"Confirmo"</strong>
                    </p>
                </td>
            </tr>
        </table>

        <!-- Signature -->
        <p style="margin: 0; font-size: 15px; color: #475569;">
            Um abraço,<br />
            <strong style="color: #0f172a;">Equipa IRWT</strong>
        </p>
    """

    return BASE_TEMPLATE.format(
        title="Proposta de Aluguer - IRWT",
        logo_url=LOGO_URL,
        content=content,
    )


def generate_proposal_plain_text(
    client_name: str,
    pickup_date: date,
    return_date: date,
    pickup_location: str,
    return_location: str,
    vehicle_type: str,
    partner_name: str,
    price: float,
) -> str:
    """Generate plain text proposal email."""

    num_days = (return_date - pickup_date).days
    if num_days < 1:
        num_days = 1

    vehicle_display = _get_vehicle_display(vehicle_type)
    pickup_date_str = _format_portuguese_date(pickup_date)
    return_date_str = _format_portuguese_date(return_date)

    return f"""Olá {client_name},

Obrigado pelo seu pedido de aluguer. Temos o prazer de apresentar a seguinte proposta:

DETALHES DO ALUGUER
-------------------
Tipo de veículo: {vehicle_display}
Data de levantamento: {pickup_date_str}
Local de levantamento: {pickup_location}
Data de devolução: {return_date_str}
Local de devolução: {return_location}
Duração: {num_days} dia(s)

PRECO TOTAL: {price:.2f} EUR

TERMOS E CONDICOES
------------------
- Pagamento integral necessário no momento da confirmação
- Carta de condução válida obrigatória no levantamento
- Política de combustivel: Cheio para Cheio
- Cancelamento: Gratuito até 48 horas antes do levantamento
- Poderá ser exigida caução no momento do levantamento

Para confirmar esta reserva, basta responder a este email com "Aceito" ou "Confirmo".

Um abraço,
Equipa IRWT
"""


def generate_confirmation_html(
    client_name: str,
    pickup_date: date,
    return_date: date,
    pickup_location: str,
    return_location: str,
    vehicle_type: str,
    partner_name: str,
    price: float,
) -> str:
    """Generate professional HTML confirmation email."""

    num_days = (return_date - pickup_date).days
    if num_days < 1:
        num_days = 1

    vehicle_display = _get_vehicle_display(vehicle_type)
    pickup_date_str = _format_portuguese_date(pickup_date)
    return_date_str = _format_portuguese_date(return_date)

    content = f"""
        <!-- Success Banner -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 12px; margin-bottom: 24px;">
            <tr>
                <td style="padding: 24px; text-align: center;">
                    <div style="width: 64px; height: 64px; background-color: rgba(255,255,255,0.2); border-radius: 50%; margin: 0 auto 16px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 32px; color: #ffffff;">&#10003;</span>
                    </div>
                    <h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #ffffff;">
                        Reserva Confirmada!
                    </h1>
                </td>
            </tr>
        </table>

        <!-- Greeting -->
        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Olá <strong>{client_name}</strong>, a sua reserva foi confirmada com sucesso. Aqui estão os detalhes:
        </p>

        <!-- Booking Details Card -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8fafc; border-radius: 12px; margin-bottom: 24px;">
            <tr>
                <td style="padding: 24px;">
                    <h2 style="margin: 0 0 20px; font-size: 16px; font-weight: 600; color: #10b981; text-transform: uppercase; letter-spacing: 0.05em;">
                        Dados da Reserva
                    </h2>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Tipo de Veiculo</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{vehicle_display}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Fornecedor</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{partner_name}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Data de Levantamento</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{pickup_date_str}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Local de Levantamento</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{pickup_location}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Data de Devolucao</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{return_date_str}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Local de Devolucao</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{return_location}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Duração</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{num_days} dia(s)</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Preço Total</span>
                                <span style="font-size: 20px; font-weight: 700; color: #10b981;">{price:.2f} EUR</span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Next Steps -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #eff6ff; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #3b82f6;">
            <tr>
                <td style="padding: 20px 24px;">
                    <h3 style="margin: 0 0 12px; font-size: 14px; font-weight: 600; color: #1e40af;">Próximos Passos</h3>
                    <ul style="margin: 0; padding-left: 20px; color: #1e40af; font-size: 13px;">
                        <li style="margin-bottom: 6px;">Traga carta de condução válida no levantamento</li>
                        <li style="margin-bottom: 6px;">Chegue ao local de levantamento a horas</li>
                        <li style="margin-bottom: 0;">Guarde este email como comprovativo da sua reserva</li>
                    </ul>
                </td>
            </tr>
        </table>

        <!-- Signature -->
        <p style="margin: 0; font-size: 15px; color: #475569;">
            Obrigado por escolher a IRWT!<br /><br />
            Um abraço,<br />
            <strong style="color: #0f172a;">Equipa IRWT</strong>
        </p>
    """

    return BASE_TEMPLATE.format(
        title="Reserva Confirmada - IRWT",
        logo_url=LOGO_URL,
        content=content,
    )


def generate_confirmation_plain_text(
    client_name: str,
    pickup_date: date,
    return_date: date,
    pickup_location: str,
    return_location: str,
    vehicle_type: str,
    partner_name: str,
    price: float,
) -> str:
    """Generate plain text confirmation email."""

    num_days = (return_date - pickup_date).days
    if num_days < 1:
        num_days = 1

    vehicle_display = _get_vehicle_display(vehicle_type)
    pickup_date_str = _format_portuguese_date(pickup_date)
    return_date_str = _format_portuguese_date(return_date)

    return f"""RESERVA CONFIRMADA!

Olá {client_name},

A sua reserva foi confirmada com sucesso. Aqui estão os detalhes:

DADOS DA RESERVA
----------------
Tipo de veículo: {vehicle_display}
Fornecedor: {partner_name}
Data de levantamento: {pickup_date_str}
Local de levantamento: {pickup_location}
Data de devolução: {return_date_str}
Local de devolução: {return_location}
Duração: {num_days} dia(s)
Preço total: {price:.2f} EUR

PROXIMOS PASSOS
---------------
- Traga carta de condução válida no levantamento
- Chegue ao local de levantamento a horas
- Guarde este email como comprovativo da sua reserva

Obrigado por escolher a IRWT!

Um abraço,
Equipa IRWT
"""


def generate_missing_info_html(
    client_name: str,
    missing_fields: list[str],
) -> str:
    """Generate professional HTML email requesting missing information."""

    # Map field names to Portuguese display names (matching José's template)
    field_names = {
        "vehicle_type": "Tipologia de viatura",
        "pickup_location": "Cidade de levantamento",
        "return_location": "Cidade de devolução",
        "pickup_date": "Data e horário previsto de início do aluguer",
        "return_date": "Data e horário previsto de final do aluguer",
        "driver_name": "Nome do Condutor",
        "artist_project_event": "Nome do Artista/Projeto/Evento*",
        "client_vat": "Dados da entidade (NIF/NIPC)",
        "destination_cities": "Cidade ou cidades de destino**",
        "client_name": "O seu nome completo",
        "client_phone": "Número de telefone",
    }

    # Check if we need footnotes
    has_artist_footnote = "artist_project_event" in missing_fields
    has_destination_footnote = "destination_cities" in missing_fields

    missing_items_html = ""
    for field in missing_fields:
        display_name = field_names.get(field, field)
        missing_items_html += f'<li style="margin-bottom: 8px; font-size: 14px; color: #1e293b;">{display_name}</li>'

    # Build footnotes
    footnotes_html = ""
    if has_artist_footnote or has_destination_footnote:
        footnotes_html = '<div style="margin-top: 16px; font-size: 12px; color: #64748b; font-style: italic;">'
        if has_artist_footnote:
            footnotes_html += '<p style="margin: 0 0 4px;">* Aqui será a vossa referência a colocar na fatura (ex. Rolling Stones - Rock in Bifanas - 30 Fevereiro)</p>'
        if has_destination_footnote:
            footnotes_html += '<p style="margin: 0;">** Solicitamos alguma informação dos destinos para vos dar a melhor cotação, trabalhamos com alguns parceiros que têm um limite de km diários e outros que não permitem a saída de Portugal.</p>'
        footnotes_html += '</div>'

    greeting_name = client_name if client_name else "Cliente"

    content = f"""
        <!-- Greeting -->
        <h1 style="margin: 0 0 24px; font-size: 24px; font-weight: 700; color: #0f172a;">
            Olá {greeting_name},
        </h1>

        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Obrigado pelo seu contacto sobre o aluguer de uma carrinha. Para podermos avançar com o seu pedido, precisamos de algumas informações adicionais.
        </p>

        <!-- Missing Info Card -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #fef3c7; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #f59e0b;">
            <tr>
                <td style="padding: 24px;">
                    <h2 style="margin: 0 0 16px; font-size: 15px; font-weight: 600; color: #92400e;">
                        Informação em Falta
                    </h2>
                    <ul style="margin: 0; padding-left: 20px; list-style-type: disc;">
                        {missing_items_html}
                    </ul>
                    {footnotes_html}
                </td>
            </tr>
        </table>

        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Assim que tivermos esses detalhes, tratamos do resto e seguimos com a reserva.
        </p>

        <!-- Signature -->
        <p style="margin: 0; font-size: 15px; color: #475569;">
            Um abraço,<br />
            <strong style="color: #0f172a;">Equipa IRWT</strong>
        </p>
    """

    return BASE_TEMPLATE.format(
        title="Informação Necessaria - IRWT",
        logo_url=LOGO_URL,
        content=content,
    )


def generate_missing_info_plain_text(
    client_name: str,
    missing_fields: list[str],
) -> str:
    """Generate plain text email requesting missing information."""

    # Map field names to Portuguese display names (matching José's template)
    field_names = {
        "vehicle_type": "Tipologia de viatura",
        "pickup_location": "Cidade de levantamento",
        "return_location": "Cidade de devolução",
        "pickup_date": "Data e horário previsto de início do aluguer",
        "return_date": "Data e horário previsto de final do aluguer",
        "driver_name": "Nome do Condutor",
        "artist_project_event": "Nome do Artista/Projeto/Evento*",
        "client_vat": "Dados da entidade (NIF/NIPC)",
        "destination_cities": "Cidade ou cidades de destino**",
        "client_name": "O seu nome completo",
        "client_phone": "Número de telefone",
    }

    # Check if we need footnotes
    has_artist_footnote = "artist_project_event" in missing_fields
    has_destination_footnote = "destination_cities" in missing_fields

    missing_items = ""
    for field in missing_fields:
        display_name = field_names.get(field, field)
        missing_items += f"- {display_name}\n"

    # Build footnotes
    footnotes = ""
    if has_artist_footnote or has_destination_footnote:
        footnotes = "\n"
        if has_artist_footnote:
            footnotes += "* Aqui será a vossa referência a colocar na fatura (ex. Rolling Stones - Rock in Bifanas - 30 Fevereiro)\n"
        if has_destination_footnote:
            footnotes += "** Solicitamos alguma informação dos destinos para vos dar a melhor cotação, trabalhamos com alguns parceiros que têm um limite de km diários e outros que não permitem a saída de Portugal.\n"

    greeting_name = client_name if client_name else "Cliente"

    return f"""Olá {greeting_name},

Obrigado pelo seu contacto sobre o aluguer de uma carrinha. Para podermos avançar com o seu pedido, precisamos de algumas informações adicionais:

{missing_items}{footnotes}
Assim que tivermos esses detalhes, tratamos do resto e seguimos com a reserva.

Um abraço,
Equipa IRWT
"""


def generate_partner_request_html(
    vehicle_type: str,
    pickup_location: str,
    return_location: str,
    pickup_datetime: str,
    return_datetime: str,
    driver_name: str,
    destination_cities: Optional[str] = None,
    sender_name: str = "Equipa IRWT",
    sender_role: str = "Reservas",
    sender_email: str = "reservas.irwt@gmail.com",
    sender_phone: str = "",
) -> str:
    """Generate professional HTML email to request vehicle from rent-a-car partner."""

    destination_row = ""
    if destination_cities:
        destination_row = f"""
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Cidade ou cidades de destino</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{destination_cities}</span>
                            </td>
                        </tr>"""

    phone_line = f"<br />Telefone: {sender_phone}" if sender_phone else ""

    content = f"""
        <!-- Greeting -->
        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Exmos. Senhores,
        </p>

        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Solicitamos, por favor, a confirmação de disponibilidade e condições para o seguinte serviço de aluguer de viatura:
        </p>

        <!-- Rental Details Card -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8fafc; border-radius: 12px; margin-bottom: 24px;">
            <tr>
                <td style="padding: 24px;">
                    <h2 style="margin: 0 0 20px; font-size: 16px; font-weight: 600; color: #0891b2; text-transform: uppercase; letter-spacing: 0.05em;">
                        Detalhes do Aluguer
                    </h2>

                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Tipologia de viatura</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{vehicle_type}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Cidade de levantamento</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{pickup_location}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Cidade de devolução</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{return_location}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Data e horario previstos de inicio do aluguer</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{pickup_datetime}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Data e horario previstos de final do aluguer</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{return_datetime}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                <span style="font-size: 13px; color: #64748b; display: block; margin-bottom: 4px;">Nome do condutor</span>
                                <span style="font-size: 15px; font-weight: 600; color: #1e293b;">{driver_name}</span>
                            </td>
                        </tr>
                        {destination_row}
                    </table>
                </td>
            </tr>
        </table>

        <!-- Request Confirmation Card -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #eff6ff; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #3b82f6;">
            <tr>
                <td style="padding: 20px 24px;">
                    <h3 style="margin: 0 0 12px; font-size: 14px; font-weight: 600; color: #1e40af;">Agradecemos confirmação relativamente a:</h3>
                    <ul style="margin: 0; padding-left: 20px; color: #1e40af; font-size: 13px;">
                        <li style="margin-bottom: 6px;">Disponibilidade da viatura</li>
                        <li style="margin-bottom: 6px;">Preço de custo final</li>
                        <li style="margin-bottom: 0;">Eventuais condições ou requisitos adicionais</li>
                    </ul>
                </td>
            </tr>
        </table>

        <p style="margin: 0 0 24px; font-size: 16px; color: #475569;">
            Após confirmação, daremos seguimento ao processo.
        </p>

        <!-- Signature -->
        <p style="margin: 0; font-size: 15px; color: #475569;">
            Com os melhores cumprimentos,<br /><br />
            <strong style="color: #0f172a;">{sender_name}</strong><br />
            {sender_role}<br />
            IRWT<br />
            Email: {sender_email}{phone_line}
        </p>
    """

    return BASE_TEMPLATE.format(
        title="Pedido de confirmação de serviço - IRWT",
        logo_url=LOGO_URL,
        content=content,
    )


def generate_partner_request_plain_text(
    vehicle_type: str,
    pickup_location: str,
    return_location: str,
    pickup_datetime: str,
    return_datetime: str,
    driver_name: str,
    destination_cities: Optional[str] = None,
    sender_name: str = "Equipa IRWT",
    sender_role: str = "Reservas",
    sender_email: str = "reservas.irwt@gmail.com",
    sender_phone: str = "",
) -> str:
    """Generate plain text email to request vehicle from rent-a-car partner."""

    destination_line = f"Cidade ou cidades de destino: {destination_cities}\n" if destination_cities else ""
    phone_line = f"Telefone: {sender_phone}\n" if sender_phone else ""

    return f"""Exmos. Senhores,

Solicitamos, por favor, a confirmação de disponibilidade e condições para o seguinte serviço de aluguer de viatura:

DETALHES DO ALUGUER
-------------------
Tipologia de viatura: {vehicle_type}
Cidade de levantamento: {pickup_location}
Cidade de devolução: {return_location}
Data e horario previstos de inicio do aluguer: {pickup_datetime}
Data e horario previstos de final do aluguer: {return_datetime}
Nome do condutor: {driver_name}
{destination_line}
Agradecemos confirmação relativamente a:
- Disponibilidade da viatura
- Preço de custo final
- Eventuais condições ou requisitos adicionais

Após confirmação, daremos seguimento ao processo.

Com os melhores cumprimentos,
{sender_name}
{sender_role}
IRWT
Email: {sender_email}
{phone_line}"""


# Subject for partner request email
PARTNER_REQUEST_SUBJECT = "Pedido de confirmação de serviço - aluguer de viatura"
