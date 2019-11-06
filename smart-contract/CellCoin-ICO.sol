// define solidity version
pragma solidity ^0.5.11;

contract CellCoinICO {
    // number of cellcoin available for sale 
    uint public max_cellcoin = 1000000;
    
    // cellcoin price in USD
    uint public usd_to_cellcoin = 1000;
    
    // total number of cellcoin that has been bought by the investors
    uint public total_bought_cellcoin = 0;
    
    // mapping the investor address to its equity in cellcoin and USD
    mapping(address => uint) equity_cellcoin;
    mapping(address => uint) equity_usd;
    
    // checking if investor can buy cellcoin
    modifier can_buy_cellcoin(uint usd_invested) {
        require(usd_invested * usd_to_cellcoin + total_bought_cellcoin <= max_cellcoin);
        _;
    }
    
    // getting the equity of an investor in cellcoin
    function equity_in_cellcoin(address investor) external view returns (uint) {
        return equity_cellcoin[investor];
    }
    
    // getting the equity of an investor in USD
    function equity_in_usd(address investor) external view returns (uint) {
        return equity_usd[investor];
    }
    
    // buying cellcoin
    function buy_cellcoins(address investor, uint usd_invested) external can_buy_cellcoin(usd_invested) {
        uint bought_cellcoins = usd_invested * usd_to_cellcoin;
        equity_cellcoin[investor] += bought_cellcoins;
        equity_usd[investor] = equity_cellcoin[investor] / usd_to_cellcoin;
        total_bought_cellcoin += bought_cellcoins;
    }
    
    // selling cellcoin
    function sell_cellcoins(address investor, uint cellcoin_amount) external {
        equity_cellcoin[investor] -= cellcoin_amount;
        equity_usd[investor] = equity_cellcoin[investor] / usd_to_cellcoin;
        total_bought_cellcoin -= cellcoin_amount;
    }
    
}
