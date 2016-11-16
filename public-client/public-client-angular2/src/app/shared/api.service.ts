import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { Cookie } from 'ng2-cookies/ng2-cookies';

import 'rxjs/Rx'
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

import { Configuration } from '../app.config';
import { ServerTime, GuestbookEntry, GuestbookEntrySet, LoginResponse, TokenRequest, TokenResponse, UserInfo } from './api.model'

@Injectable()
export class ApiService {

    title:String = 'Angular 2';

    private actionUrl: string;
    private headers: Headers;

    constructor(private _http: Http, private _configuration: Configuration) {

        this.actionUrl = _configuration.ApiBaseUrl;

        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
    }


    public getServerTime = (): Observable<ServerTime> => {
        return this._http.get(this.actionUrl + 'time', { headers: this.headers })
            .map((response: Response) => <ServerTime>response.json())
            .catch(this.handleError);
    }

    public signGuestbook = (entry: GuestbookEntry): Observable<GuestbookEntry> => {
        // post to the API with the supplied entry
        let bodyString = JSON.stringify(entry);
        return this._http.post(this.actionUrl + 'guestbook', bodyString, { headers: this.headers })
            .map((response: Response) => <GuestbookEntry>response.json())
            .catch(this.handleError);
    }

    public browseGuestbook = (): Observable<GuestbookEntrySet> => {
        // retrieve the most recent guestbook entries
        return this._http.get(this.actionUrl + 'guestbook', { headers: this.headers })
            .map((response: Response) => <GuestbookEntrySet>response.json())
            .catch(this.handleError);
    }

    public browseGuestbookMore = (last_id: string): Observable<GuestbookEntrySet> => {
        // retrieve the most recent guestbook entries since the id provided
        return this._http.get(this.actionUrl + 'guestbook?last_id='+last_id, { headers: this.headers })
            .map((response: Response) => <GuestbookEntrySet>response.json())
            .catch(this.handleError);
    }

    public startLogin = (): Observable<LoginResponse> => {
        // call the login start api service to get the info needed to start the login process
        return this._http.get(this.actionUrl + 'login', { headers: this.headers })
            .map((response: Response) => <LoginResponse>response.json())
            .catch(this.handleError);
    }

    public claimTokens = (request: TokenRequest): Observable<TokenResponse> => {
        // call the api token service to get the auth tokens
        let bodyString = JSON.stringify(request);
        return this._http.post(this.actionUrl + 'login/token', bodyString, { headers: this.headers })
            .map((response: Response) => <TokenResponse>response.json())
            .catch(this.handleError);
    }

    public getUserInfo = (): Observable<UserInfo> => {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('Authorization', Cookie.get('wzstarter.oidc.id_token'));
        return this._http.get(this.actionUrl + 'login/info', {headers: headers})
            .map((response: Response) => <UserInfo>response.json())
            .catch(this.handleError);
    }


    private handleError(error: Response) {
        console.error(error);
        return Observable.throw(error.json().error || 'Server error');
    }
}
