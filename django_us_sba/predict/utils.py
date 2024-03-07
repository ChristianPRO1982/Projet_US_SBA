def process_validation(process_location: bool,
                       process_bank: bool,
                       process_activity: bool,
                       process_bank_loan: bool,
                       process_guaranteed_amount_requested: bool) -> bool:
    if process_location and process_bank and process_activity and process_bank_loan and process_guaranteed_amount_requested:
        return 2
    return 1