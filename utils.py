import constants as cons


def filter_by_age(age, session_min_age_limit):
    if age is None:
        return True
    elif 18 <= int(age) < 45 and session_min_age_limit == 18:
        return True
    elif int(age) >= 45 and session_min_age_limit == 45:
        return True
    else:
        return False


def filter_by_fee(fee, session_fee):
    if fee is None:
        return True
    else:
        return fee == session_fee


def filter_by_dose(dose_type, session, min_available=1):
    if dose_type is None:
        return session['available_capacity'] >= min_available
    else:
        return int(session[cons.doses[dose_type]]) >= min_available


def filter_by_vaccine(vaccine, session_vaccine):
    if vaccine is None:
        return True
    else:
        return vaccine == session_vaccine


def filter_user_pref(user, fee_type, session):
    return filter_by_dose(user['dose_type'], session, user['min_available']) and filter_by_age(user['age'], session[
        "min_age_limit"]) and filter_by_fee(user['fee'], fee_type) and filter_by_vaccine(user['vaccine'],
                                                                                         session['vaccine'])
