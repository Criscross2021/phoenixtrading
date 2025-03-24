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

        # Fetch exchange rates dynamically
        self.EXCHANGE_RATES = get_exchange_rates()

    def convert_to_tonnes(self, quantity, unit, commodity):
        """
        Convert the given quantity to tonnes based on the unit and commodity.

        Args:
            quantity (float): The quantity to convert.
            unit (str): The unit of measurement (e.g., "tonnes", "bushels").
            commodity (str): The selected commodity (e.g., "soybeans").

        Returns:
            float: The quantity converted to tonnes.
        """
        if commodity not in self.UNIT_CONVERSIONS:
            raise ValueError(f"Invalid commodity: {commodity}")
        if unit not in self.UNIT_CONVERSIONS[commodity]:
            raise ValueError(f"Invalid unit for {commodity}: {unit}")
        return quantity * self.UNIT_CONVERSIONS[commodity][unit]

    def convert_usd_to_brl(self, amount_usd):
        """
        Convert the given amount in USD to BRL.

        Args:
            amount_usd (float): The amount in USD.

        Returns:
            float: The amount converted to BRL.
        """
        return amount_usd * self.EXCHANGE_RATES["BRL"]

    def convert_usd_to_eur(self, amount_usd):
        """
        Convert the given amount in USD to EUR.

        Args:
            amount_usd (float): The amount in USD.

        Returns:
            float: The amount converted to EUR.
        """
        return amount_usd * self.EXCHANGE_RATES["EUR"]

    def convert_usd_to_yuan(self, amount_usd):
        """
        Convert the given amount in USD to CNY (Yuan).

        Args:
            amount_usd (float): The amount in USD.

        Returns:
            float: The amount converted to CNY.
        """
        return amount_usd * self.EXCHANGE_RATES["CNY"]

    def calculate_total_cost(self, quantity, unit, commodity, trade_term, cost_params):
        """
        Calculate the total cost for the given quantity of the selected commodity and trade term.

        Args:
            quantity (float): The quantity of the commodity.
            unit (str): The unit of measurement (e.g., "tonnes").
            commodity (str): The selected commodity (e.g., "soybeans").
            trade_term (str): The selected trade term (e.g., "FOB Storage").
            cost_params (dict): A dictionary of cost parameters.

        Returns:
            dict: A dictionary containing the cost breakdown.
        """
        # Convert quantity to tonnes
        quantity_tonnes = self.convert_to_tonnes(quantity, unit, commodity)

        # Calculate costs
        purchase_price = quantity_tonnes * cost_params.get("purchase_price_per_unit", 0)
        processing_fee = quantity_tonnes * cost_params.get("processing_fee_per_unit", 0)
        trucking_farm_to_storage = quantity_tonnes * cost_params.get("trucking_farm_to_storage_per_unit", 0)
        storage_fee = quantity_tonnes * cost_params.get("storage_fee_per_unit", 0)
        loading_containers_rls = cost_params.get("loading_containers_rls", 0)

        trucking_storage_to_port = quantity_tonnes * cost_params.get("trucking_storage_to_port_per_unit", 0)
        truck_free_time_hours = cost_params.get("truck_free_time_hours", 0)
        truck_free_time_rls = cost_params.get("truck_free_time_rls", 0)
        empty_containers = cost_params.get("empty_containers", 0)
        truck_unloading_rls = cost_params.get("truck_unloading_rls", 0)
        terminal_free_time_days = cost_params.get("terminal_free_time_days", 0)
        storage_fee_port = quantity_tonnes * cost_params.get("storage_fee_port_per_unit", 0)
        port_handling_fee = quantity_tonnes * cost_params.get("port_handling_per_unit", 0)
        ad_valorem = cost_params.get("ad_valorem", 0)
        ICMS_unit = cost_params.get("ICMS_unit", 0)

        ocean_freight = quantity_tonnes * cost_params.get("ocean_freight_per_tonne", 0)
        carrier_security_fee = quantity_tonnes * cost_params.get("carrier_security_fee_per_tonne", 0)
        bunker_recovery_charge = quantity_tonnes * cost_params.get("bunker_recovery_charge_per_tonne", 0)
        pilotage_service_cost = quantity_tonnes * cost_params.get("pilotage_service_cost_per_tonne", 0)
        demurrage_load = cost_params.get("demurrage_load_per_day", 0) * cost_params.get("demurrage_load_days", 0)
        detention_load = cost_params.get("detention_load_per_day", 0) * cost_params.get("detention_load_days", 0)
        ship_owner_free_time_days = cost_params.get("ship_owner_free_time_days", 0)
        terminal_handling_charge_load = quantity_tonnes * cost_params.get("terminal_handling_charge_load_per_tonne", 0)
        ship_port_security = quantity_tonnes * cost_params.get("ship_port_security_per_tonne", 0)
        documentation_fee = cost_params.get("documentation_fee", 0)
        seal_fee = cost_params.get("seal_fee", 0)
        insurance_cost = quantity_tonnes * cost_params.get("insurance_per_tonne", 0) if trade_term == "CIF" else 0

        destination_port_fee = quantity_tonnes * cost_params.get("terminal_handling_charge_disport_per_tonne", 0)
        delivery_order_fee = cost_params.get("delivery_order_fee", 0)
        inland_transport_destination = quantity_tonnes * cost_params.get("inland_transport_destination_per_tonne", 0)
        storage_fee_destination = quantity_tonnes * cost_params.get("storage_fee_destination_per_tonne", 0)
        detention_discharge_days = cost_params.get("detention_discharge_days", 0) * cost_params.get("detention_per_day_load", 0)

        # Sum up all costs
        total_cost_usd = (
            purchase_price
            + processing_fee
            + trucking_farm_to_storage
            + storage_fee
            + loading_containers_rls
            + trucking_storage_to_port
            + truck_free_time_hours
            + truck_free_time_rls
            + empty_containers
            + truck_unloading_rls
            + terminal_free_time_days
            + storage_fee_port
            + port_handling_fee
            + ad_valorem
            + ICMS_unit
            + ocean_freight
            + carrier_security_fee
            + bunker_recovery_charge
            + pilotage_service_cost
            + demurrage_load
            + detention_load
            + ship_owner_free_time_days
            + terminal_handling_charge_load
            + ship_port_security
            + documentation_fee
            + seal_fee
            + insurance_cost
            + destination_port_fee
            + delivery_order_fee
            + inland_transport_destination
            + storage_fee_destination
            + detention_discharge_days
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