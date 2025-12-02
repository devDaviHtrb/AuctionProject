payment_statuses_data = [
    {"payment_status": "payment_authorized",                     "payment_name": "Autorizado"},
    {"payment_status": "payment_approved_by_risk_analysis",      "payment_name": "Aprovado Por Análise"},
    {"payment_status": "payment_created",                        "payment_name": "Criado"},
    {"payment_status": "payment_confirmed",                      "payment_name": "Confirmado"},
    {"payment_status": "payment_anticipated",                    "payment_name": "Antecipado"},
    {"payment_status": "payment_deleted",                        "payment_name": "Excluído"},
    {"payment_status": "payment_refunded",                       "payment_name": "Reembolsado"},
    {"payment_status": "payment_refund_denied",                  "payment_name": "Reembolso Negado"},
    {"payment_status": "payment_chargeback_requested",           "payment_name": "Chargeback Solicitado"},
    {"payment_status": "payment_awaiting_chargeback_reversal",   "payment_name": "Aguardando Reversão"},
    {"payment_status": "payment_dunning_requested",              "payment_name": "Negativação Solicitada"},
    {"payment_status": "payment_checkout_viewed",                "payment_name": "Checkout Visualizado"},
    {"payment_status": "payment_partially_refunded",             "payment_name": "Reembolso Parcial"},
    {"payment_status": "payment_split_divergence_block",         "payment_name": "Bloqueio Por Divergência"},
    {"payment_status": "payment_awaiting_risk_analysis",         "payment_name": "Aguardando Análise"},
    {"payment_status": "payment_reproved_by_risk_analysis",      "payment_name": "Reprovado Por Análise"},
    {"payment_status": "payment_updated",                        "payment_name": "Atualizado"},
    {"payment_status": "payment_received",                       "payment_name": "Recebido"},
    {"payment_status": "payment_overdue",                        "payment_name": "Vencido"},
    {"payment_status": "payment_restored",                       "payment_name": "Restaurado"},
    {"payment_status": "payment_refund_in_progress",             "payment_name": "Reembolso Em Andamento"},
    {"payment_status": "payment_received_in_cash_undone",        "payment_name": "Estorno Em Dinheiro"},
    {"payment_status": "payment_chargeback_dispute",             "payment_name": "Disputa Chargeback"},
    {"payment_status": "payment_dunning_received",               "payment_name": "Negativação Recebida"},
    {"payment_status": "payment_bank_slip_viewed",               "payment_name": "Boleto Visualizado"},
    {"payment_status": "payment_credit_card_capture_refused",    "payment_name": "Captura Recusada"},
    {"payment_status": "payment_split_cancelled",                "payment_name": "Split Cancelado"},
    {"payment_status": "payment_split_divergence_block_finished","payment_name": "Bloqueio Finalizado"},
]

payment_methods_data = [
    {"payment_method": "pix"},
    {"payment_method": "boleto"},
    {"payment_method": "cartão de crédito"},
    {"payment_method": "cartão de débito"},
    {"payment_method": "ted"},
    {"payment_method": "indefinido"}
]

case_types_data = [
    {"case_type_name": "fiscal"},
    {"case_type_name": "judicial"},
]

categories_data = [
    {"category_name": "outros"},
    {"category_name": "eletronicos"},
    {"category_name": "artes"},
    {"category_name": "antiguidades"},
    {"category_name": "joias"},
    {"category_name": "veiculos"},
    {"category_name": "imoveis"}
]

technical_features_data = [
    {"technical_feature_name": "peso"},
    {"technical_feature_name": "dimensoes"},
    {"technical_feature_name": "material"},
    {"technical_feature_name": "ano de fabricacao"},
    {"technical_feature_name": "cor"},
    {"technical_feature_name": "estado de conservacao"},
    {"technical_feature_name": "garantia"},
    {"technical_feature_name": "marca"},
    {"technical_feature_name": "modelo"},
    {"technical_feature_name": "voltagem"}
]

category_technical_features_data = [
    {"technical_feature_id": 1,  "category_id": 1},
    {"technical_feature_id": 2,  "category_id": 1},
    {"technical_feature_id": 3,  "category_id": 1},
    {"technical_feature_id": 4,  "category_id": 1},
    {"technical_feature_id": 5,  "category_id": 1},
    {"technical_feature_id": 6,  "category_id": 1},
    {"technical_feature_id": 7,  "category_id": 1},
    {"technical_feature_id": 8,  "category_id": 1},
    {"technical_feature_id": 9,  "category_id": 1},
    {"technical_feature_id": 10, "category_id": 1},

    {"technical_feature_id": 1,  "category_id": 2},
    {"technical_feature_id": 2,  "category_id": 2},
    {"technical_feature_id": 7,  "category_id": 2},
    {"technical_feature_id": 8,  "category_id": 2},
    {"technical_feature_id": 9,  "category_id": 2},
    {"technical_feature_id": 10, "category_id": 2},

    {"technical_feature_id": 1,  "category_id": 3},
    {"technical_feature_id": 2,  "category_id": 3},
    {"technical_feature_id": 3,  "category_id": 3},
    {"technical_feature_id": 6,  "category_id": 3},

    {"technical_feature_id": 1,  "category_id": 4},
    {"technical_feature_id": 2,  "category_id": 4},
    {"technical_feature_id": 3,  "category_id": 4},
    {"technical_feature_id": 4,  "category_id": 4},
    {"technical_feature_id": 6,  "category_id": 4},

    {"technical_feature_id": 1,  "category_id": 5},
    {"technical_feature_id": 3,  "category_id": 5},
    {"technical_feature_id": 5,  "category_id": 5},
    {"technical_feature_id": 6,  "category_id": 5},

    {"technical_feature_id": 4,  "category_id": 6},
    {"technical_feature_id": 5,  "category_id": 6},
    {"technical_feature_id": 8,  "category_id": 6},
    {"technical_feature_id": 9,  "category_id": 6},
    {"technical_feature_id": 7,  "category_id": 6},

    {"technical_feature_id": 2,  "category_id": 7},
    {"technical_feature_id": 6,  "category_id": 7},
    {"technical_feature_id": 4,  "category_id": 7},
]
