import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import {Router, ActivatedRoute} from '@angular/router';
import { OIDCService } from '../oidc.service'
import {Subscription} from "rxjs";
import {TimerObservable} from "rxjs/observable/TimerObservable";


@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {

    private sub: Subscription;

    constructor(private oidc: OIDCService, private activatedRoute: ActivatedRoute) {

    }

    handleLoginClick(): void {
        this.oidc.login();
    }

    isLoggedIn(): boolean {
        return this.oidc.isLoggedIn();
    }

    ngOnInit() {
        this.sub = this.activatedRoute.queryParams.subscribe(params => {
            let code = params["code"];
            if (code != null) {
                console.log("Handling IDP callback");
                let state = params["state"]
                if (state == null) {
                    throw new Error("Missing state in idp callback");
                }
                this.oidc.claimTokens(code, state);
            }
        });
    }

    ngOnDestroy() {
        this.sub.unsubscribe();
    }
}