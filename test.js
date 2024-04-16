import Two from 'https://cdn.skypack.dev/two.js@latest';

const two = new Two({
    type: Two.Types.canvas,
    width: 1024,
    height: 1024,
    autostart: true
}).appendTo(document.body);

const x = two.width / 2;
const y = two.height / 2;

const enchantment_glint = two.makeTexture('assets/img/mc/Enchanted_Item_Glint.png');
enchantment_glint.repeat = 'repeat';
enchantment_glint.offset.x = 0;
enchantment_glint.scale = 4;

const item = two.makeSprite('assets/img/mc/Bread.png', x, y);

const styles = {
  size: 50,
};
const text = two.makeText('Hello World', x, y, styles);


two.update();