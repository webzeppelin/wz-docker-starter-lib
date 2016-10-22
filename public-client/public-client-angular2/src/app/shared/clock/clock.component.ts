import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ServerTime } from '../api.model'
import { ApiService } from '../api.service'
import {Subscription} from "rxjs";
import {TimerObservable} from "rxjs/observable/TimerObservable";


@Component({
  selector: 'clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.scss']
})
export class ClockComponent implements OnInit {

    server_time: ServerTime;
    tick: Number;
    subscription: Subscription;

    constructor(private api: ApiService) {
        // Do something with api
    }

    observeServerTime(): void {
        this.api.getServerTime()
            .subscribe(
                st => this.setServerTime(st),
                error => console.error('Error: ' + error),
                () => console.log('Completed!')
            )
    }

    setServerTime(st: ServerTime): void {
        this.server_time = st;
    }

    get formatted_time() {
        return ClockComponent.fnum(this.server_time.hour) + ' : '
            + ClockComponent.fnum(this.server_time.minute) + ' : '
            + ClockComponent.fnum(this.server_time.second);
    }

    static fnum(num: Number) {
        if (num < 10) return '0'+num;
        return ''+num;
    }

    ngOnInit() {
        this.observeServerTime();
        let timer = TimerObservable.create(1000, 1000);
        this.subscription = timer.subscribe(t => {
            this.tick = t;
            this.server_time.second++;
            if (this.server_time.second > 59) {
                this.server_time.second = 0;
                this.server_time.minute++;
                if (this.server_time.minute > 59) {
                    this.server_time.minute = 0;
                    this.server_time.hour++;
                    if (this.server_time.hour > 23) {
                        this.server_time.hour = 0;
                    }
                }
            }
        });
    }

    ngOnDestroy() {
        this.subscription.unsubscribe();
    }
}