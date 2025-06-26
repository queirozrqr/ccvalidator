import re

class CreditCardValidator:
    """Classe para validar números de cartão de crédito e identificar bandeiras"""
    
    def __init__(self):
        # Padrões para identificar cada bandeira
        self.card_patterns = {
            'Visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
            'MasterCard': r'^5[1-5][0-9]{14}$|^2[2-7][0-9]{14}$',
            'American Express': r'^3[47][0-9]{13}$',
            'Diners Club': r'^3[0689][0-9]{11}$|^54[0-9]{14}$|^55[0-9]{14}$',
            'Discover': r'^6(?:011|5[0-9]{2})[0-9]{12}$',
            'enRoute': r'^2(?:014|149)[0-9]{11}$',
            'JCB': r'^(?:2131|1800|35\d{3})\d{11}$',
            'Voyager': r'^8699[0-9]{11}$',
            'HiperCard': r'^(?:606282\d{10}(\d{3})?|3841\d{15})$',
            'Aura': r'^50[0-9]{14}$'
        }
    
    def clean_card_number(self, card_number):
        """Remove espaços, hífens e outros caracteres não numéricos"""
        return re.sub(r'[^0-9]', '', str(card_number))
    
    def luhn_algorithm(self, card_number):
        """Implementa o algoritmo de Luhn para validar o número do cartão"""
        def digits_of(number):
            return [int(d) for d in str(number)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        checksum = sum(odd_digits)
        for digit in even_digits:
            checksum += sum(digits_of(digit * 2))
        
        return checksum % 10 == 0
    
    def identify_card_brand(self, card_number):
        """Identifica a bandeira do cartão baseado no número"""
        clean_number = self.clean_card_number(card_number)
        
        for brand, pattern in self.card_patterns.items():
            if re.match(pattern, clean_number):
                return brand
        
        return "Bandeira não identificada"
    
    def validate_card(self, card_number):
        """Valida o cartão de crédito e retorna informações completas"""
        clean_number = self.clean_card_number(card_number)
        
        # Verifica se tem apenas dígitos
        if not clean_number.isdigit():
            return {
                'valid': False,
                'brand': None,
                'error': 'Número deve conter apenas dígitos'
            }
        
        # Verifica comprimento mínimo
        if len(clean_number) < 13 or len(clean_number) > 19:
            return {
                'valid': False,
                'brand': None,
                'error': 'Número deve ter entre 13 e 19 dígitos'
            }
        
        # Identifica a bandeira
        brand = self.identify_card_brand(clean_number)
        
        # Valida usando algoritmo de Luhn
        is_luhn_valid = self.luhn_algorithm(clean_number)
        
        return {
            'valid': is_luhn_valid and brand != "Bandeira não identificada",
            'brand': brand if brand != "Bandeira não identificada" else None,
            'luhn_valid': is_luhn_valid,
            'error': None if is_luhn_valid and brand != "Bandeira não identificada" else 
                    'Número inválido pelo algoritmo de Luhn' if not is_luhn_valid else 
                    'Bandeira não suportada'
        }

def main():
    """Função principal para interação com o usuário"""
    validator = CreditCardValidator()
    
    print("=" * 50)
    print("     VALIDADOR DE CARTÃO DE CRÉDITO")
    print("=" * 50)
    print("\nBandeiras suportadas:")
    print("• Visa")
    print("• MasterCard")
    print("• American Express")
    print("• Diners Club")
    print("• Discover")
    print("• enRoute")
    print("• JCB")
    print("• Voyager")
    print("• HiperCard")
    print("• Aura")
    print("\n" + "=" * 50)
    
    while True:
        print("\nDigite o número do cartão de crédito (ou 'sair' para encerrar):")
        card_input = input("Número: ").strip()
        
        if card_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o programa...")
            break
        
        if not card_input:
            print("❌ Por favor, digite um número válido.")
            continue
        
        # Valida o cartão
        result = validator.validate_card(card_input)
        
        print("\n" + "-" * 40)
        print("RESULTADO DA VALIDAÇÃO:")
        print("-" * 40)
        
        if result['valid']:
            print(f"✅ Cartão VÁLIDO")
            print(f"🏷️  Bandeira: {result['brand']}")
        else:
            print(f"❌ Cartão INVÁLIDO")
            if result['brand']:
                print(f"🏷️  Bandeira identificada: {result['brand']}")
            if result['error']:
                print(f"❗ Erro: {result['error']}")
        
        print(f"🔍 Validação Luhn: {'✅ Passou' if result['luhn_valid'] else '❌ Falhou'}")
        print("-" * 40)

def test_cards():
    """Função para testar com números de exemplo"""
    validator = CreditCardValidator()
    
    # Números de teste (alguns válidos pelo algoritmo de Luhn)
    test_numbers = [
        "4532015112830366",  # Visa
        "5555555555554444",  # MasterCard
        "378282246310005",   # American Express
        "30569309025904",    # Diners Club
        "6011111111111117",  # Discover
        "4111111111111111",  # Visa
        "5105105105105100",  # MasterCard
    ]
    
    print("\n" + "=" * 50)
    print("     TESTE COM NÚMEROS DE EXEMPLO")
    print("=" * 50)
    
    for card in test_numbers:
        result = validator.validate_card(card)
        status = "✅ VÁLIDO" if result['valid'] else "❌ INVÁLIDO"
        brand = result['brand'] if result['brand'] else "Não identificada"
        print(f"Cartão: {card}")
        print(f"Status: {status} | Bandeira: {brand}")
        print("-" * 30)

if __name__ == "__main__":
    # Pergunta se o usuário quer executar testes ou validação interativa
    print("Escolha uma opção:")
    print("1 - Validação interativa")
    print("2 - Executar testes com números de exemplo")
    
    choice = input("Digite sua escolha (1 ou 2): ").strip()
    
    if choice == "2":
        test_cards()
    else:
        main()