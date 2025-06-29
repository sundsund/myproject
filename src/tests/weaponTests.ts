import { expect } from 'chai';
import { Weapon, BulletFactory } from '../lib/weapon';

describe('Weapon', () => {
    var subject: Weapon;
    var shotsFired: number = 0;
    var capturedArgs: any = null; // Variable to store captured arguments

    // Mocked bullet factory
    var bulletFactoryMock: BulletFactory = <BulletFactory>{
        generate: function(px, py, vx, vy, rot) {
            shotsFired++;
            capturedArgs = { px, py, vx, vy, rot }; // Capture args
        }
    };
    // Updated parent mock to include rotation
    var parentMock: any = { x: 0, y: 0, rotation: 0 };

    beforeEach(() => {
        shotsFired = 0;
        capturedArgs = null; // Reset captured args for each test
        subject = new Weapon(bulletFactoryMock, parentMock, 0.25, 1); // Use updated mocks
    });

    it('should shoot if not in cooldown and pass correct arguments', () => {
        subject.trigger(true);
        subject.update(0.1); // Weapon timer is initially 0, so 0.1 makes it -0.1, thus shoots
        expect(shotsFired).to.equal(1);

        // Assertions for captured arguments
        expect(capturedArgs).to.not.be.null;
        expect(capturedArgs.px).to.be.a('number').and.not.be.NaN;
        expect(capturedArgs.py).to.be.a('number').and.not.be.NaN;
        expect(capturedArgs.vx).to.be.a('number').and.not.be.NaN;
        expect(capturedArgs.vy).to.be.a('number').and.not.be.NaN;
        expect(capturedArgs.rot).to.be.a('number').and.not.be.NaN;

        // Specific checks based on parentMock = {x:0, y:0, rotation:0} and weapon constructor bulletSpeed = 1
        // In Weapon.shoot():
        // parentRotation = parentMock.rotation + Math.PI / 2 = 0 + Math.PI / 2 = Math.PI / 2
        // velx_calc = Math.cos(Math.PI / 2) => approx 0 (actually a very small number close to 0)
        // vely_calc = Math.sin(Math.PI / 2) => approx 1
        // posx = parentMock.x - velx_calc * 10
        // posy = parentMock.y - vely_calc * 10
        // Bullet speed is 1. Velocities passed are -velx_calc * bulletSpeed and -vely_calc * bulletSpeed.
        // Expected args for bulletFactory.generate: rot=0 (parentMock.rotation)
        expect(capturedArgs.px).to.be.closeTo(parentMock.x - Math.cos(parentMock.rotation + Math.PI / 2) * 10, 0.00001);
        expect(capturedArgs.py).to.be.closeTo(parentMock.y - Math.sin(parentMock.rotation + Math.PI / 2) * 10, 0.00001);
        expect(capturedArgs.vx).to.be.closeTo(-Math.cos(parentMock.rotation + Math.PI / 2) * 1, 0.00001);
        expect(capturedArgs.vy).to.be.closeTo(-Math.sin(parentMock.rotation + Math.PI / 2) * 1, 0.00001);
        expect(capturedArgs.rot).to.equal(parentMock.rotation);
    });

    it('should not shoot during cooldown', () => {
        subject.trigger(true);
        subject.update(0.1);
        subject.update(0.1);
        expect(shotsFired).to.equal(1);
    });

    it('should shoot after cooldown ends', () => {
        subject.trigger(true);
        subject.update(0.1);
        subject.update(0.3); // longer than timeout
        expect(shotsFired).to.equal(2);
    });

    it('should not shoot if not triggered', () => {
        subject.update(0.1);
        subject.update(0.1);
        expect(shotsFired).to.equal(0);
    });
});
