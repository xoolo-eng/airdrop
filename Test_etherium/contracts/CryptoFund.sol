pragma solidity ^0.4.24;

import "./ERC20.sol";

contract CryptoFundToken is MintableToken {
    using SafeMath for uint256;
    string public constant name = "CryptoFund Token";
    string public constant symbol = "CHU";
    uint8 public constant decimals = 18;
    // количество токенов в обороте
    uint public totalFunds;
    // возращенные токены
    mapping (address => uint) withdraws;

    function CryptoFundToken(uint _funds) Ownable() external {
        require (_funds > 0);
        totalFunds = _funds;
    }

    function foundsOf() external constant returns (uint) {
        return totalFunds;
    }

    function supplyOf() external constant returns (uint) {
        return totalSupply;
    }

    // количесво уничтоженых токенов
    function withdrawOf(address _owner) external constant returns (uint) {
        return withdraws[_owner];
    }

    // создание токенов
    // @param address _to - для кого выпущены
    // @param uint _amount - сколько выпущено
    // @param uint _cost - заплачено ETH
    function release(address _to, uint _amount, uint _cost) onlyOwner external {
        mint(_to, _amount);
        totalFunds = totalFunds.add(_cost);
    }

    // уничтожение токенов
    // @param address _from - кто вернул
    // @param uint _amount - сколько вернули
    // @param uint _cost - выплачено ETH
    function withdraw(address _from, uint _amount, uint _cost) onlyOwner external {
        balances[_from] = balances[_from].sub(_amount);
        totalSupply = totalSupply.sub(_amount);
        withdraws[_from] = withdraws[_from].add(_amount);
        totalFunds = totalFunds.sub(_cost);
    }

    // рассылка уже купленых токенов
    // @param address[] _to - список адресов
    // @param uint[] _amount - количество токенов
    function dispatch(address[] _to, uint[] _amount) onlyOwner external {
        require (_to.length == _amount.length);
        for(uint i=0; i<_to.length;++i) {
            mint(_to[i], _amount[i]);
        }
    }
