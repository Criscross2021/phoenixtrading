from utils.currency_rate import get_exchange_rates

class CommodityTrade:
    def __init__(self):
        # Constants for unit conversions
        self.UNIT_CONVERSIONS = {
            "soybeans": {
                "bushels": 0.0272155,  # 1 bushel = 0.0272155 tonnes
                "sacks": 0.06,  # 1 sack = 60 kg = 0.06 tonnes
                "tonnes": 1,
            },
            "sugar": {
                "bags": 0.05,  # 1 bag = 50 kg = 0.05 tonnes
                "tonnes": 1,
            },
            "maize": {
                "bushels": 0.0254,  # 1 bushel = 0.0254 tonnes
                "tonnes": 1,
            },
            "soybean_oil": {
                "liters": 0.00092,  # 1 liter = 0.92 kg = 0.00092 tonnes
                "tonnes": 1,
            },
        }

        # Exchange rates (now handles BRL/USD explicitly)
        self.EXCHANGE_RATES = get_exchange_rates()
        self.BRL_TO_USD = 1 / self.EXCHANGE_RATES["BRL"]

    def convert_to_tonnes(self, quantity, unit, commodity):
        """Unchanged from original"""
        if commodity not in self.UNIT_CONVERSIONS:
            raise ValueError(f"Invalid commodity: {commodity}")
        if unit not in self.UNIT_CONVERSIONS[commodity]:
            raise ValueError(f"Invalid unit for {commodity}: {unit}")
        return quantity * self.UNIT_CONVERSIONS[commodity][unit]

    def _convert_to_usd(self, amount, currency):
        """Helper: Convert any currency to USD"""
        if currency == "BRL":
            return amount * self.BRL_TO_USD
        return amount  # Assume USD

    def calculate_total_cost(self, quantity, unit, commodity, trade_term, cost_params):
        """
        Updated to handle currency-aware cost_params: {field: (value, currency)}
        """
        quantity_tonnes = self.convert_to_tonnes(quantity, unit, commodity)

        # Extract values with currency conversion
        def get_cost(field, default_currency="USD"):
            value, currency = cost_params.get(field, (0.0, default_currency))
            return {
                "USD": value * (self.BRL_TO_USD if currency == "BRL" else 1),
                "original": value,
                "currency": currency
            }

        # --- Farm Costs (now handles BRL properly) ---
        purchase_price = get_cost("purchase_price") * quantity_tonnes
        processing_fee = get_cost("processing_fee") * quantity_tonnes
        trucking_farm_to_storage = get_cost("trucking_farm_to_storage") * quantity_tonnes
        storage_fee = get_cost("storage_fee_farm") * quantity_tonnes
        loading_containers = get_cost("loading_containers")

        # --- Port Costs ---
        trucking_storage_to_port = get_cost("trucking_storage_to_port") * quantity_tonnes
        truck_free_time_hours = get_cost("truck_free_time_hours")
        truck_free_time_rls = get_cost("truck_free_time_rls")
        empty_containers = get_cost("empty_containers")
        unloading_containers = get_cost("unloading_containers")
        terminal_free_time_days = get_cost("terminal_free_time_days")
        storage_fee_port = get_cost("storage_fee_port") * quantity_tonnes
        port_handling_fee = get_cost("port_handling") * quantity_tonnes
        ad_valorem = get_cost("ad_valorem")
        icms = get_cost("icms")

        # --- Ocean Costs ---
        ocean_freight = get_cost("ocean_freight") * quantity_tonnes
        carrier_security_fee = get_cost("carrier_security_fee") * quantity_tonnes
        bunker_recovery_charge = get_cost("bunker_recovery_charge") * quantity_tonnes
        pilotage_service_cost = get_cost("pilotage_service_cost") * quantity_tonnes
        demurrage_load = get_cost("demurrage_rate") * get_cost("demurrage_days")
        detention_load = get_cost("detention_rate") * get_cost("detention_days")
        ship_owner_free_time_days = get_cost("ship_owner_free_time")
        terminal_handling_charge_load = get_cost("terminal_handling_charge") * quantity_tonnes
        ship_port_security = get_cost("ship_port_security") * quantity_tonnes
        documentation_fee = get_cost("documentation_fee")
        seal_fee = get_cost("seal_fee")
        insurance_cost = get_cost("insurance") * quantity_tonnes if trade_term == "CIF" else 0

        # --- Destination Costs ---
        destination_port_fee = get_cost("terminal_handling_disport") * quantity_tonnes
        delivery_order_fee = get_cost("delivery_order_fee")
        inland_transport_destination = get_cost("inland_transport_destination") * quantity_tonnes
        storage_fee_destination = get_cost("storage_fee_destination") * quantity_tonnes
        detention_discharge_days = get_cost("detention_destination")

        # --- Totals ---
        total_cost_usd = (
                purchase_price + processing_fee + trucking_farm_to_storage +
                storage_fee + loading_containers + trucking_storage_to_port +
                truck_free_time_hours + truck_free_time_rls + empty_containers +
                unloading_containers + terminal_free_time_days + storage_fee_port +
                port_handling_fee + ad_valorem + icms + ocean_freight +
                carrier_security_fee + bunker_recovery_charge + pilotage_service_cost +
                demurrage_load + detention_load + ship_owner_free_time_days +
                terminal_handling_charge_load + ship_port_security + documentation_fee +
                seal_fee + insurance_cost + destination_port_fee + delivery_order_fee +
                inland_transport_destination + storage_fee_destination + detention_discharge_days
        )

        # Calculate total cost per metric tonne
        total_cost_per_tonne = total_cost_usd / quantity_tonnes

        # Convert total cost to BRL, EUR, and CNY
        total_cost_brl = self.convert_usd_to_brl(total_cost_usd)
        total_cost_eur = self.convert_usd_to_eur(total_cost_usd)
        total_cost_yuan = self.convert_usd_to_yuan(total_cost_usd)

        # Return cost breakdown
        return {
            "Purchase Price": purchase_price,
            "Processing Fee": processing_fee,
            "Trucking (Farm to Storage)": trucking_farm_to_storage,
            "Storage Fee": storage_fee,
            "Loading Containers (RLS)": loading_containers_rls,
            "Trucking (Storage to Port)": trucking_storage_to_port,
            "Truck Free Time (Hours)": truck_free_time_hours,
            "Truck Free Time (RLS)": truck_free_time_rls,
            "Empty Containers": empty_containers,
            "Truck Unloading (RLS)": truck_unloading_rls,
            "Terminal Free Time (Days)": terminal_free_time_days,
            "Storage Fee (Port)": storage_fee_port,
            "Port Handling Fee": port_handling_fee,
            "Ad Valorem": ad_valorem,
            "ICMS": ICMS_unit,
            "Ocean Freight": ocean_freight,
            "Carrier Security Fee": carrier_security_fee,
            "Bunker Recovery Charge": bunker_recovery_charge,
            "Pilotage Service Cost": pilotage_service_cost,
            "Demurrage (Load)": demurrage_load,
            "Detention (Load)": detention_load,
            "Ship Owner Free Time (Days)": ship_owner_free_time_days,
            "Terminal Handling Charge (Load)": terminal_handling_charge_load,
            "Ship and Port Security": ship_port_security,
            "Documentation Fee": documentation_fee,
            "Seal Fee": seal_fee,
            "Insurance": insurance_cost,
            "Destination Port Fee": destination_port_fee,
            "Delivery Order Fee": delivery_order_fee,
            "Inland Transport (Destination)": inland_transport_destination,
            "Storage Fee at Destination": storage_fee_destination,
            "Detention at Destination": detention_discharge_days,
            "Total Cost (USD)": total_cost_usd,
            "Total Cost (BRL)": total_cost_brl,
            "Total Cost (EUR)": total_cost_eur,
            "Total Cost (CNY)": total_cost_yuan,
            "Total Cost per Tonne (USD)": total_cost_per_tonne,
        }
