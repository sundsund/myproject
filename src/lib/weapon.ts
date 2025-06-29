export class Weapon {
    private isTriggered: boolean = false;
    private currentTimer: number = 0;

    constructor(private bulletFactory: BulletFactory, private parent: Phaser.Sprite, private cooldown: number, private bulletSpeed: number) {
    }

    public trigger(on: boolean): void {
        this.isTriggered = on;
    }

    public update(delta: number): void {
        this.currentTimer -= delta;

        if (this.isTriggered && this.currentTimer <= 0) {
            this.shoot();
        }
    }

    private shoot(): void {
        // Reset timer
        this.currentTimer = this.cooldown;

        // Get velocity direction from player rotation
        var parentRotation = this.parent.rotation + Math.PI / 2;
        var velx = Math.cos(parentRotation);
        var vely = Math.sin(parentRotation);

        // Apply a small forward offset so bullet shoots from head of ship instead of the middle
        var posx = this.parent.x - velx * 10
        var posy = this.parent.y - vely * 10;

        this.bulletFactory.generate(posx, posy, -velx * this.bulletSpeed, -vely * this.bulletSpeed, this.parent.rotation);
    }
}

export class BulletFactory {

    constructor(private bullets: Phaser.Group, private poolSize: number) {
        this.bullets.enableBody = true;
        this.bullets.physicsBodyType = Phaser.Physics.ARCADE;
        this.bullets.createMultiple(30, 'bullet');
        this.bullets.setAll('anchor.x', 0.5);
        this.bullets.setAll('anchor.y', 0.5);
        this.bullets.setAll('outOfBoundsKill', true);
        this.bullets.setAll('checkWorldBounds', true);
    }

    public generate(posx: number, posy: number, velx: number, vely: number, rot: number): Phaser.Sprite {
        var bullet = this.bullets.getFirstExists(false);

        if (bullet) {
            bullet.reset(posx, posy);
            bullet.rotation = rot;
            bullet.body.velocity.x = velx;
            bullet.body.velocity.y = vely;
        }

        return bullet;
    }
}
